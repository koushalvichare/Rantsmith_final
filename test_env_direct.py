#!/usr/bin/env python3
"""Direct test of .env loading"""

import os
from dotenv import load_dotenv

# Clear any existing env var
if 'SECRET_KEY' in os.environ:
    del os.environ['SECRET_KEY']

print("Before loading .env:")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY', 'NOT_SET')}")

# Load .env
load_dotenv()

print("\nAfter loading .env:")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY', 'NOT_SET')}")

# Check if .env file exists
if os.path.exists('.env'):
    print("\n.env file exists")
    with open('.env', 'r') as f:
        lines = f.readlines()
        secret_lines = [line.strip() for line in lines if line.startswith('SECRET_KEY')]
        print(f"SECRET_KEY lines in .env: {secret_lines}")
else:
    print("\n.env file does not exist!")
