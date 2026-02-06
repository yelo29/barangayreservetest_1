import sqlite3

# Connect to database
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Update the user table to include profile_photo_url if it doesn't exist
try:
    cursor.execute('ALTER TABLE users ADD COLUMN profile_photo_url TEXT')
    print("Added profile_photo_url column to users table")
except:
    print("profile_photo_url column already exists")

# Update saloestillopez@gmail.com (ID 14) with the profile photo from verification_requests
cursor.execute('''
    UPDATE users 
    SET profile_photo_url = (
        SELECT user_photo_url 
        FROM verification_requests 
        WHERE resident_id = 14 
        ORDER BY submitted_at DESC 
        LIMIT 1
    )
    WHERE id = 14
''')

conn.commit()
conn.close()

print("Updated user 14 (saloestillopez@gmail.com) with profile photo from verification_requests")
