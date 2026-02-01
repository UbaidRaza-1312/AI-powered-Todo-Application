import os
from dotenv import load_dotenv
load_dotenv()

print(f"Current DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set - will use default')}")
print(f"Default fallback: sqlite+aiosqlite:///./todo_app_local.db")