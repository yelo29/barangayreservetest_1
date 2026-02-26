import requests

print('=== TESTING VERIFICATION STATUS FOR NON-RESIDENT ===')

# Test the verification status endpoint for unresident@gmail.com (user ID 32)
user_id = 32
response = requests.get(f'http://192.168.100.4:8000/api/verification-requests/status/{user_id}')

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'✅ Verification Status Response:')
    print(f'   - Can Submit: {data.get("can_submit")}')
    print(f'   - Lock Message: "{data.get("lock_message")}"')
    print(f'   - Current Status: {data.get("current_status")}')
    print(f'   - Verified: {data.get("verified")}')
    print(f'   - Verification Type: {data.get("verification_type")}')
    
    # Verify the fix
    can_submit = data.get('can_submit', False)
    lock_message = data.get('lock_message', '')
    current_status = data.get('current_status', '')
    
    if can_submit and 'upgrade to Resident status' in lock_message:
        print('✅ SUCCESS: Verified non-resident can now submit verification request!')
    elif not can_submit and 'Non-Resident with limited benefits' in lock_message:
        print('❌ FAILED: Still blocking verified non-residents')
    else:
        print(f'⚠️  UNEXPECTED: can_submit={can_submit}, message="{lock_message}"')
else:
    print(f'❌ Error: {response.text}')

print('\nEXPECTED BEHAVIOR:')
print('✅ Can Submit: true')
print('✅ Lock Message: "You can submit a verification request to upgrade to Resident status"')
print('✅ Current Status: verified_non_resident')
