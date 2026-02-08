import sqlite3

def check_apology_message():
    """Check if apology message was properly set in rejected bookings"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING APOLOGY MESSAGE IN REJECTED BOOKINGS ===")
    
    # Check specific booking that was auto-rejected (ID 63)
    cursor.execute('''
        SELECT id, booking_date, facility_id, status, rejection_reason, purpose, updated_at
        FROM bookings 
        WHERE id = 63
    ''')
    
    booking = cursor.fetchone()
    
    if booking:
        print(f"📋 Booking ID: {booking[0]}")
        print(f"📅 Date: {booking[1]}")
        print(f"🏢 Facility: {booking[2]}")
        print(f" Status: {booking[3]}")
        print(f"💬 Rejection Reason: '{booking[4]}'")
        print(f"🎯 Purpose: {booking[5]}")
        print(f"⏰ Updated At: {booking[6]}")
        
        if booking[4] and "apologize" in booking[4].lower():
            print("✅ Apology message FOUND in rejection_reason")
        else:
            print("❌ Apology message MISSING in rejection_reason")
    else:
        print("❌ Booking ID 63 not found")
    
    # Check all rejected bookings for apology messages
    print("\n=== ALL REJECTED BOOKINGS WITH APOLOGY MESSAGES ===")
    cursor.execute('''
        SELECT id, booking_date, facility_id, status, rejection_reason, purpose, updated_at
        FROM bookings 
        WHERE status = 'rejected' AND rejection_reason IS NOT NULL
        ORDER BY updated_at DESC
        LIMIT 10
    ''')
    
    rejected_bookings = cursor.fetchall()
    
    if rejected_bookings:
        print(f"📊 Found {len(rejected_bookings)} rejected bookings with rejection reasons:")
        for booking in rejected_bookings:
            print(f"  ID {booking[0]}: {booking[1]} - Facility {booking[2]} - '{booking[4][:50]}...' ({booking[6]})")
    else:
        print("❌ No rejected bookings with rejection reasons found")
    
    conn.close()

if __name__ == "__main__":
    check_apology_message()
