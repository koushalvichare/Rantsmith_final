import os
import sys
from app import create_app

def main():
    """Main function to run the application"""
    try:
        # Create the Flask app
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        
        print("🚀 Starting RantSmith AI...")
        print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
        print(f"Debug mode: {app.config['DEBUG']}")
        print("=" * 50)
        
        # Run the application
        app.run(
            host=os.getenv('HOST', '127.0.0.1'),
            port=int(os.getenv('PORT', 5000)),
            debug=app.config['DEBUG']
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n🔧 Try installing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Application Error: {e}")
        print("\n🔧 Try running the test script first:")
        print("python test_app.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
