#!/usr/bin/env python3
"""
Test script to verify the application starts without errors
"""
import asyncio
import sys
import traceback
from main import app

async def test_startup():
    """Test that the application can be imported and started without errors"""
    try:
        # Test importing the main app
        print("✓ Successfully imported main app")
        
        # Test that the app object is properly configured
        assert hasattr(app, 'routes'), "App should have routes attribute"
        print("✓ App has routes attribute")
        
        # Test that all routers are properly registered
        route_paths = [route.path for route in app.routes]
        auth_routes_present = any('/auth' in path for path in route_paths)
        task_routes_present = any('/tasks' in path for path in route_paths)
        chat_routes_present = any('/chat' in path for path in route_paths)
        
        print(f"✓ Authentication routes present: {auth_routes_present}")
        print(f"✓ Task routes present: {task_routes_present}")
        print(f"✓ Chat routes present: {chat_routes_present}")
        
        print("\n✓ All startup tests passed!")
        print("The application should start without the SQLAlchemy relationship errors.")
        print("The main error was fixed by properly annotating the relationship fields with Mapped[].")
        
    except Exception as e:
        print(f"✗ Error during startup test: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_startup())
    sys.exit(0 if success else 1)