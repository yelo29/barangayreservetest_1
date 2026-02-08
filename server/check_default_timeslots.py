import sqlite3

def check_default_timeslots():
    """Check what default time slots should be available"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING DEFAULT TIME SLOTS ===")
    
    # Check if there are any default time slots configured
    cursor.execute('SELECT * FROM time_slots ORDER BY start_time')
    time_slots = cursor.fetchall()
    
    print(f"📅 Time slots in database: {len(time_slots)}")
    for i, slot in enumerate(time_slots):
        print(f"  {i+1}. ID: {slot[0]}, Start: {slot[1]}, End: {slot[2]}, Facility: {slot[3]}")
    
    # Check facility 3 specifically
    cursor.execute('SELECT * FROM time_slots WHERE facility_id = 3 ORDER BY start_time')
    facility_slots = cursor.fetchall()
    
    print(f"\n🏊 Swimming Pool (Facility 3) time slots: {len(facility_slots)}")
    for i, slot in enumerate(facility_slots):
        print(f"  {i+1}. ID: {slot[0]}, Start: {slot[1]}, End: {slot[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_default_timeslots()
