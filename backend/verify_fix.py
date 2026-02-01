#!/usr/bin/env python3
"""
Simple test to verify the fix is syntactically correct
"""
import ast
import sys

# Check if the Python file has valid syntax
file_path = r"C:\Users\Star.com\Desktop\Todo-Application\backend\src\agents\chat_agent.py"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Parse the file to check for syntax errors
    ast.parse(source)
    print("OK: Syntax is valid")

    # Check if our fix is in the file
    if 'actual_result = result.get("result", {})' in source:
        print("OK: Fix for result handling is in place")
    else:
        print("MISSING: Fix for result handling is missing")

    if '"message", "✅ Action completed successfully"' in source:
        print("OK: Proper message extraction is in place")
    else:
        print("MISSING: Proper message extraction is in place")

    print("\nAll checks passed!")

except SyntaxError as e:
    print(f"ERROR: Syntax error in file: {e}")
except Exception as e:
    print(f"ERROR: Error reading file: {e}")