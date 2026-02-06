import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get user ID for saloestillopez@gmail.com
cursor.execute('SELECT id FROM users WHERE email = "saloestillopez@gmail.com"')
user_result = cursor.fetchone()
user_id = user_result[0] if user_result else None

print(f'User ID for saloestillopez@gmail.com: {user_id}')

if user_id:
    # Check verification requests for this user
    cursor.execute('SELECT * FROM verification_requests WHERE resident_id = ? ORDER BY submitted_at DESC LIMIT 1', (user_id,))
    request = cursor.fetchone()
    print('\nLatest verification request:')
    if request:
        columns = [description[0] for description in cursor.description]
        for i, col in enumerate(columns):
            if col in ['profile_photo_url', 'profilePhotoUrl', 'profilePhoto', 'profile_image', 'profileImage', 'avatar', 'photo_url', 'imageUrl']:
                # Show first 100 characters of base64 data
                value = str(request[i])[:100] + "..." if len(str(request[i])) > 100 else request[i]
                print(f'{col}: {value}')
            else:
                print(f'{col}: {request[i]}')
    else:
        print('No verification request found')

    print('\n' + '='*50 + '\n')

    # Check current user data
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    print('Current user data:')
    if user:
        columns = [description[0] for description in cursor.description]
        for i, col in enumerate(columns):
            if col in ['profile_photo_url', 'profilePhotoUrl', 'profilePhoto', 'profile_image', 'profileImage', 'avatar', 'photo_url', 'imageUrl']:
                # Show first 100 characters of base64 data
                value = str(user[i])[:100] + "..." if len(str(user[i])) > 100 else user[i]
                print(f'{col}: {value}')
            else:
                print(f'{col}: {user[i]}')
    else:
        print('No user found')

conn.close()
