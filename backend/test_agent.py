"""
Test script to check if the AI agent properly recognizes tools
"""
import os
import google.generativeai as genai
from src.mcp.server import mcp_server
from src.agents.system_prompt import SYSTEM_PROMPT
import inspect

def get_mcp_tools():
    """Replicate the same tool generation as in the chat agent"""
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

def test_ai_model():
    print("=== AI AGENT TEST ===")
    
    # Get tools as the agent does
    tools = get_mcp_tools()
    print(f"Tools sent to AI model: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {list(tool['parameters']['properties'].keys())}")
    
    # Configure the AI model
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment")
        return
    
    genai.configure(api_key=api_key)
    
    # Create model with tools and system prompt
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
        tools=[{"function_declarations": tools}],
    )
    
    # Test conversation
    chat = model.start_chat()
    
    # Test message
    test_message = """
    USER CONTEXT (ALREADY VERIFIED — DO NOT ASK AGAIN):
    user_id: 5807fcba-83e4-4328-b0ea-6c851ea2db99

    USER MESSAGE:
    delete task2
    """
    
    print(f"\nSending test message to AI model:")
    print(test_message)
    
    try:
        response = chat.send_message(test_message)

        print(f"\nAI Response candidates:")
        for i, candidate in enumerate(response.candidates):
            print(f"  Candidate {i}: finish_reason = {candidate.finish_reason.name}")

            if hasattr(candidate, 'content') and candidate.content.parts:
                for j, part in enumerate(candidate.content.parts):
                    if hasattr(part, 'function_call'):
                        print(f"    Part {j}: Function call detected")
                        print(f"      Name: {part.function_call.name}")
                        print(f"      Args: {dict(part.function_call.args)}")
                    elif hasattr(part, 'text'):
                        print(f"    Part {j}: Text response")
                        print(f"      Text: {part.text}")
                    else:
                        print(f"    Part {j}: Other type: {type(part)}")
            else:
                print(f"  Candidate {i}: No content parts")

    except Exception as e:
        print(f"Error testing AI model: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_model()