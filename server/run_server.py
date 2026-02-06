#!/usr/bin/env python3
"""
Simple Server Runner
Starts the Flask server with proper configuration
"""

import sys
import os
import subprocess
from config import Config

def main():
    print("🚀 Starting Barangay Reserve Server...")
    print(f"📊 Database: {Config.DATABASE_PATH}")
    print(f"🌐 Server will run on: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'server_updated.py'
    env['FLASK_ENV'] = 'development'
    env['SERVER_HOST'] = '127.0.0.1'
    env['SERVER_PORT'] = '5000'
    env['DEBUG'] = 'True'
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, 'server_updated.py'], env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
