import sqlite3

def check_booking_structure():
    """Check the structure of booking data"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING BOOKING STRUCTURE ===")
    
    # Get the latest resident booking (ID 53)
    cursor.execute('''
        SELECT id, start_time, end_time, status, booking_date
        FROM bookings 
        WHERE id = 53
    ''')
    
    booking = cursor.fetchone()
    if booking:
        booking_id, start_time, end_time, status, date = booking
        print(f"Booking ID: {booking_id}")
        print(f"Start Time: '{start_time}'")
        print(f"End Time: '{end_time}'")
        print(f"Status: {status}")
        print(f"Date: {date}")
        
        print(f"\nData types:")
        print(f"  start_time type: {type(start_time)}")
        print(f"  end_time type: {type(end_time)}")
        
        # Check if start_time already contains the full timeslot
        if ' - ' in str(start_time):
            print(f"✅ start_time already contains full timeslot: '{start_time}'")
        else:
            print(f"❌ start_time needs to be combined with end_time")
    
    conn.close()

if __name__ == "__main__":
    check_booking_structure()
