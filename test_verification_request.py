import requests
import json

def test_verification_request():
    base_url = 'http://192.168.100.4:8000'
    
    print('🚀 TESTING VERIFICATION REQUEST FIX')
    print('=' * 50)
    
    # Test verification request submission
    verification_data = {
        'residentId': 33,  # neverresident@gmail.com user ID
        'fullName': 'John Leo L. Lopez',
        'contactNumber': '09656692463',
        'address': 'Mountain',
        'verificationType': 'non-resident',
        'userPhotoUrl': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABkAJDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAIDAAQABECEiMRMEEiBVEVYnEjFhBxJxkaGx0fBhciEjJ0Kx8RVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwA/9k=',
        'validIdUrl': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABkAJDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAIDAAQABECEiMRMEEiBVEVYnEjFhBxJxkaGx0fBhciEjJ0Kx8RVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwA/9k=',
        'submittedAt': '2026-02-26T16:40:00'
    }
    
    try:
        print(f'🔍 Submitting verification request for User ID: {verification_data["residentId"]}')
        print(f'  - Verification Type: {verification_data["verificationType"]}')
        print(f'  - Full Name: {verification_data["fullName"]}')
        
        response = requests.post(f'{base_url}/api/verification-requests', json=verification_data, timeout=10)
        
        print(f'\n📊 Response Status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'✅ Success: {result.get("success")}')
            print(f'📝 Message: {result.get("message")}')
            
            if result.get('success'):
                print('🎉 VERIFICATION REQUEST SUBMITTED SUCCESSFULLY!')
            else:
                print(f'❌ VERIFICATION REQUEST FAILED: {result.get("message")}')
        else:
            print(f'❌ HTTP Error: {response.status_code}')
            print(f'📝 Response: {response.text}')
            
    except Exception as e:
        print(f'❌ Error: {e}')
    
    print('\n🎯 TEST COMPLETED')

if __name__ == '__main__':
    test_verification_request()
