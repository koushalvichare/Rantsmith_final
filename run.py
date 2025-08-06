import os
import sys

# Set UTF-8 encoding for stdout and stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from app import create_app

# Create the Flask app instance for Gunicorn
app = create_app(os.getenv('FLASK_ENV', 'production'))

def main():
    """Main function to run the application in development"""
    try:
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
        print("\n🔧 This might be due to a missing dependency or an incorrect import path.")
        print("   Try installing dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Application Error: {e}")
        print("\n🔧 An unexpected error occurred. Please check the logs for more details.")
        sys.exit(1)

if __name__ == '__main__':
    main()
