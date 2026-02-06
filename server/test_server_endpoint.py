import requests

# Test if the server is actually using SQLite or still using Firebase
base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

print("Testing server endpoints to identify backend type...")

# Test the home endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"Home endpoint: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Home endpoint error: {e}")

print("\n" + "="*50 + "\n")

# Test a simple SQLite endpoint
try:
    response = requests.get(f"{base_url}/api/me?email=secretary@barangay.gov")
    print(f"API /me endpoint: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"API /me endpoint error: {e}")

print("\n" + "="*50 + "\n")

# Test facilities endpoint
try:
    response = requests.get(f"{base_url}/api/facilities")
    print(f"Facilities endpoint: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Facilities count: {len(data) if isinstance(data, list) else 'N/A'}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Facilities endpoint error: {e}")

print("\n" + "="*50 + "\n")

# Test if this is a Firebase-based server by checking for Firebase-style responses
try:
    # Try a Firebase-style endpoint
    response = requests.post(
        f"{base_url}/api/login",
        json={'email': 'test@test.com', 'password': 'test'},
        headers={'Content-Type': 'application/json'}
    )
    print(f"Alternative login endpoint: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Alternative login endpoint error: {e}")
