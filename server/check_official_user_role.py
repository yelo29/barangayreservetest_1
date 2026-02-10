import sqlite3

def check_official_user_role():
    """Check the official user role detection"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING OFFICIAL USER ROLE DETECTION ===")
    
    # Check the official user
    cursor.execute('''
        SELECT u.id, u.email, u.role
        FROM users u
        WHERE u.email = 'captain@barangay.gov'
    ''')
    
    official_user = cursor.fetchone()
    if official_user:
        user_id, email, role = official_user
        print(f"👤 Official user info:")
        print(f"   ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Role: {role}")
        
        is_official = role == 'official'
        print(f"   is_official_booking = {is_official}")
    
    # Check how the user_id is retrieved in the booking creation
    cursor.execute('''
        SELECT id FROM users WHERE email = 'captain@barangay.gov'
    ''')
    
    user_id_result = cursor.fetchone()
    if user_id_result:
        retrieved_user_id = user_id_result[0]
        print(f"\n🔍 Retrieved user_id for captain@barangay.gov: {retrieved_user_id}")
        
        # Check if this matches the booking's user_id
        cursor.execute('''
            SELECT user_id FROM bookings WHERE id = 34
        ''')
        
        booking_user_id = cursor.fetchone()
        if booking_user_id:
            booking_user_id = booking_user_id[0]
            print(f"🔍 Booking 34 user_id: {booking_user_id}")
            print(f"🔍 User IDs match: {retrieved_user_id == booking_user_id}")
    
    conn.close()

if __name__ == "__main__":
    check_official_user_role()
