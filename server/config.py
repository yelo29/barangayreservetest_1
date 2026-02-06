# Dynamic Server Configuration for DuckDNS
import os

# Load environment variables from .env file
def _load_env():
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    except Exception as e:
        print(f"⚠️  Could not load .env file: {e}")

# Load environment variables at import
_load_env()

class Config:
    """Server configuration that works with any IP/DuckDNS setup"""
    
    # Server settings
    HOST = os.getenv('SERVER_HOST', '0.0.0.0')  # Accept all connections
    PORT = int(os.getenv('SERVER_PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # CORS settings - Allow all origins for DuckDNS flexibility
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Database settings
    DATABASE_PATH = os.getenv('DB_PATH', 'barangay.db')
    
    # DuckDNS settings (from environment)
    DUCKDNS_DOMAIN = os.getenv('DUCKDNS_DOMAIN', '')
    DUCKDNS_TOKEN = os.getenv('DUCKDNS_TOKEN', '')
    
    @classmethod
    def get_server_url(cls):
        """Get the server URL based on environment or default"""
        if DUCKDNS_DOMAIN:
            return f"https://{DUCKDNS_DOMAIN}"
        else:
            # Fallback to local detection
            return f"http://localhost:{cls.PORT}"
    
    @classmethod
    def get_cors_origins(cls):
        """Get CORS origins for Flutter app"""
        if cls.CORS_ORIGINS == '*':
            return ['*']  # Allow all origins
        else:
            return [origin.strip() for origin in cls.CORS_ORIGINS.split(',')]

# Environment variables for easy configuration
ENV_VARS = {
    'SERVER_HOST': '0.0.0.0',
    'SERVER_PORT': '8080', 
    'DEBUG': 'False',
    'CORS_ORIGINS': '*',
    'DB_PATH': 'barangay.db',
    'DUCKDNS_DOMAIN': 'your-domain.duckdns.org',
    'DUCKDNS_TOKEN': 'your-duckdns-token'
}
