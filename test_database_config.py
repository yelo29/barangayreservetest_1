import requests
import json
import os

# Test database configuration
BASE_URL = "http://192.168.100.4:8000"

def test_database_config():
    """Test database configuration"""
    print("🗄️ TESTING DATABASE CONFIGURATION")
    print("=" * 50)
    
    # Check current database path
    server_config_path = os.path.join(os.path.dirname(__file__), 'server', 'config.py')
    print(f"Server config path: {server_config_path}")
    
    # Check if database exists in server folder
    server_db_path = os.path.join(os.path.dirname(__file__), 'server', 'barangay.db')
    root_db_path = os.path.join(os.path.dirname(__file__), 'barangay.db')
    
    print(f"Server database exists: {os.path.exists(server_db_path)}")
    print(f"Root database exists: {os.path.exists(root_db_path)}")
    
    if os.path.exists(server_db_path):
        size = os.path.getsize(server_db_path)
        print(f"Server database size: {size} bytes")
    
    if os.path.exists(root_db_path):
        size = os.path.getsize(root_db_path)
        print(f"Root database size: {size} bytes")

def test_server_health():
    """Test if server is running"""
    print("\n🏥 TESTING SERVER HEALTH")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilities", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responsive")
            return True
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error checking server health: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DATABASE CONFIGURATION TEST")
    print("=" * 60)
    
    test_database_config()
    
    if test_server_health():
        print("\n✅ Server is ready for testing!")
    else:
        print("\n❌ Please start the server first:")
        print("   cd server")
        print("   python server.py")
    
    print("=" * 60)
