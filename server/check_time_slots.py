import sqlite3

def check_time_slots():
    """Check available time slots for Community Hall"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== CHECKING TIME SLOTS FOR COMMUNITY HALL ===")
    
    cursor.execute('''
        SELECT id, start_time, end_time FROM time_slots 
        WHERE facility_id = 1 
        ORDER BY sort_order
    ''')
    
    time_slots = cursor.fetchall()
    print(f"Found {len(time_slots)} time slots:")
    
    for ts in time_slots:
        ts_id, start_time, end_time = ts
        print(f"  ID {ts_id}: {start_time} - {end_time}")
    
    conn.close()

if __name__ == "__main__":
    check_time_slots()
