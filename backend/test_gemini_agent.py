import asyncio
import os
from src.agents.chat_agent import ChatAgent

async def test_agent():
    # Print the API key status
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"GEMINI_API_KEY is set: {bool(api_key and api_key.strip())}")
    
    agent = ChatAgent()
    print(f"Agent uses Gemini: {getattr(agent, 'use_gemini', False)}")
    
    try:
        result = await agent.process_message('test_user', 'Hello, how are you?')
        print('Response:', result['response'])
        print('Tool calls:', result['tool_calls'])
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())