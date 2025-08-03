#!/usr/bin/env python3
"""
Setup script for RantSmith AI
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        try:
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your actual API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        # Create basic .env file
        env_content = """SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///rantsmith.db
OPENAI_API_KEY=your-openai-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
RUNWAYML_API_KEY=your-runwayml-api-key-here
"""
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ Created basic .env file")
            print("📝 Please edit .env file with your actual API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False

def create_uploads_folder():
    """Create uploads folder"""
    if not os.path.exists('uploads'):
        try:
            os.makedirs('uploads')
            print("✅ Created uploads folder")
        except Exception as e:
            print(f"❌ Failed to create uploads folder: {e}")
            return False
    else:
        print("✅ Uploads folder already exists")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up RantSmith AI...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Try manually:")
        print("pip install -r requirements.txt")
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Create uploads folder
    if not create_uploads_folder():
        return
    
    # Initialize database
    if not run_command("python create_db.py", "Initializing database"):
        print("⚠️ Database initialization failed, but you can try running manually:")
        print("python create_db.py")
    
    # Run tests
    if not run_command("python test_app.py", "Running application tests"):
        print("⚠️ Tests failed, but you can still try running the application")
    
    print("\n🎉 Setup completed!")
    print("\n🚀 To start the application:")
    print("python run.py")
    print("\n📝 Don't forget to:")
    print("1. Edit the .env file with your API keys")
    print("2. Check the application at http://localhost:5000")

if __name__ == '__main__':
    main()
