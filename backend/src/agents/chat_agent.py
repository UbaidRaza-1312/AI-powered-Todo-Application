"""
Chat Agent for AI Chatbot with MCP Integration
FINAL STABLE VERSION – safe Gemini handling, user context, tool loop correct
"""

import os
import uuid
import inspect
import re
import google.generativeai as genai
from typing import Dict, Any, List

from sqlmodel import select
from ..mcp.server import mcp_server
from ..agents.system_prompt import SYSTEM_PROMPT
from ..db.database import get_session_maker
from ..models.message import Message
from ..models.user import User


# -----------------------------
# MCP tools → Gemini schema
# -----------------------------
def get_mcp_tools():
    tools = []

    for name, func in mcp_server.tools.items():
        sig = inspect.signature(func)
        schema = {"type": "object", "properties": {}, "required": []}

        for param in sig.parameters.values():
            if param.default == inspect.Parameter.empty:
                schema["required"].append(param.name)
            schema["properties"][param.name] = {"type": "string"}

        tools.append({
            "name": name,
            "description": func.__doc__ or name,
            "parameters": schema,
        })

    return tools


# -----------------------------
# Safe text extraction
# -----------------------------
def extract_text(candidate) -> str:
    if not candidate or not hasattr(candidate, "content"):
        return ""

    content = candidate.content
    if not content or not hasattr(content, "parts") or not content.parts:
        return ""

    texts = [part.text for part in content.parts if hasattr(part, "text") and part.text]
    return "".join(texts).strip()


# =============================
# Chat Agent
# =============================
class ChatAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=[{"function_declarations": get_mcp_tools()}],
        )

    # -----------------------------
    # Load conversation history
    # -----------------------------
    async def get_conversation_history(self, conversation_id: str):
        session_maker = get_session_maker()
        async with session_maker() as session:
            stmt = select(Message).where(
                Message.conversation_id == uuid.UUID(conversation_id)
            ).order_by(Message.created_at.asc())

            result = await session.execute(stmt)
            messages = result.scalars().all()[-20:]  # limit history

            history = []
            for msg in messages:
                gemini_role = "model" if msg.role == "assistant" else "user"
                history.append({
                    "role": gemini_role,
                    "parts": [msg.content],
                })
            return history

    # -----------------------------
    # Fetch user info
    # -----------------------------
    async def get_user_info(self, user_id: str):
        session_maker = get_session_maker()
        async with session_maker() as session:
            return await session.get(User, uuid.UUID(user_id))

    # -----------------------------
    # Main message processor
    # -----------------------------
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: str,
    ) -> Dict[str, Any]:

        # Validate UUIDs
        try:
            uuid.UUID(user_id)
            uuid.UUID(conversation_id)
        except ValueError:
            return {
                "response": "Invalid session. Please log in again.",
                "tool_calls": []
            }

        session_maker = get_session_maker()

        # Save USER message
        async with session_maker() as session:
            session.add(Message(
                id=uuid.uuid4(),
                user_id=uuid.UUID(user_id),
                conversation_id=uuid.UUID(conversation_id),
                role="user",
                content=message
            ))
            await session.commit()

        # Load history
        history = await self.get_conversation_history(conversation_id)
        chat = self.model.start_chat(history=history)

        # -----------------------------
        # FAST PATH: Delete intercept
        # -----------------------------
        delete_pattern = r'(?:delete|remove)\s+(?:task)\s+(\d+|"[^"]+"|\'.*?\'|\w+)'
        delete_match = re.search(delete_pattern, message.lower().strip())

        if delete_match and len(message.split()) < 8:
            task_reference = delete_match.group(1).strip('"').strip("'")

            tool_args = {
                "task_reference": f"task {task_reference}",
                "user_id": user_id
            }

            result = await mcp_server.execute_tool("delete_task_by_reference", tool_args)
            tool_calls = [result]

            final_text = "❌ Failed to delete task"
            if result["success"]:
                tool_result = result["result"]
                if isinstance(tool_result, dict):
                    final_text = tool_result.get("message", "✅ Task deleted successfully")

            async with session_maker() as session:
                session.add(Message(
                    id=uuid.uuid4(),
                    user_id=uuid.UUID(user_id),
                    conversation_id=uuid.UUID(conversation_id),
                    role="assistant",
                    content=final_text
                ))
                await session.commit()

            return {"response": final_text, "tool_calls": tool_calls}

        # -----------------------------
        # Build prompt with user context
        # -----------------------------
        user = await self.get_user_info(user_id)

        # Construct full name from first and last name
        first_name = user.first_name if user and user.first_name else ""
        last_name = user.last_name if user and user.last_name else ""
        user_name = f"{first_name} {last_name}".strip() if (first_name or last_name) else "Unknown"

        user_email = user.email if user and user.email else "Unknown"

        prompt = f"""
USER CONTEXT (ALREADY VERIFIED — DO NOT ASK AGAIN):
user_id: {user_id}
name: {user_name}
email: {user_email}

USER MESSAGE:
{message}
"""

        tool_calls: List[Dict[str, Any]] = []

        try:
            response = await chat.send_message_async(prompt)

            if not response.candidates:
                raise ValueError("No candidates returned from Gemini")

            candidate = response.candidates[0]

            # -----------------------------
            # Detect tool calls safely
            # -----------------------------
            tool_requests = []
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        tool_requests.append(part.function_call)

            # -----------------------------
            # TOOL LOOP
            # -----------------------------
            if tool_requests:
                tool_responses = []

                for call in tool_requests:
                    fn = call.name
                    args = dict(call.args)
                    args["user_id"] = user_id

                    result = await mcp_server.execute_tool(fn, args)
                    tool_calls.append(result)

                    tool_responses.append({
                        "function_response": {
                            "name": fn,
                            "response": result
                        }
                    })

                # Send tool results back to Gemini
                response = await chat.send_message_async(tool_responses)

                if response.candidates:
                    final_text = extract_text(response.candidates[0])
                else:
                    final_text = ""

            else:
                final_text = extract_text(candidate)

            if not final_text:
                final_text = "✅ Action completed successfully" if tool_calls else \
                             "I’m here and ready. What would you like to do next?"

        except Exception as e:
            final_text = f"I hit an error while processing that: {str(e)}"
            tool_calls = []

        # Save ASSISTANT message
        async with session_maker() as session:
            session.add(Message(
                id=uuid.uuid4(),
                user_id=uuid.UUID(user_id),
                conversation_id=uuid.UUID(conversation_id),
                role="assistant",
                content=final_text
            ))
            await session.commit()

        return {
            "response": final_text,
            "tool_calls": tool_calls
        }
