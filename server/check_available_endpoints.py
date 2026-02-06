import requests

base_url = "https://intershifting-nakisha-nonspaciously.ngrok-free.dev"

print("Checking available login endpoints...")

# Test different possible login endpoints
endpoints_to_test = [
    "/api/auth/login",
    "/api/login", 
    "/login",
    "/auth/login",
    "/api/signin",
    "/signin"
]

for endpoint in endpoints_to_test:
    try:
        response = requests.post(
            f"{base_url}{endpoint}",
            json={'email': 'test@test.com', 'password': 'test'},
            headers={'Content-Type': 'application/json'}
        )
        print(f"POST {endpoint}: {response.status_code}")
        if response.status_code != 404:
            print(f"  Response: {response.text[:200]}...")
    except Exception as e:
        print(f"POST {endpoint}: Error - {e}")

print("\n" + "="*50 + "\n")

# Test GET requests too
for endpoint in endpoints_to_test:
    try:
        response = requests.get(f"{base_url}{endpoint}")
        print(f"GET {endpoint}: {response.status_code}")
        if response.status_code != 404:
            print(f"  Response: {response.text[:200]}...")
    except Exception as e:
        print(f"GET {endpoint}: Error - {e}")

print("\n" + "="*50 + "\n")

# Check what endpoints are available by trying common ones
common_endpoints = [
    "/",
    "/api",
    "/api/users",
    "/api/bookings",
    "/api/facilities",
    "/health",
    "/status"
]

for endpoint in common_endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}")
        print(f"GET {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"GET {endpoint}: Error - {e}")
