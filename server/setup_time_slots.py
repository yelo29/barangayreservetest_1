import sqlite3

def setup_time_slots():
    """Setup default time slots for all facilities"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== SETTING UP TIME SLOTS ===")
    
    # Default time slots (start, end, duration in minutes)
    default_slots = [
        ("6:00 AM", "8:00 AM", 120),
        ("8:00 AM", "10:00 AM", 120),
        ("10:00 AM", "12:00 PM", 120),
        ("12:00 PM", "2:00 PM", 120),
        ("2:00 PM", "4:00 PM", 120),
        ("4:00 PM", "6:00 PM", 120),
        ("6:00 PM", "8:00 PM", 120),
        ("8:00 PM", "10:00 PM", 120),
    ]
    
    # Get all facilities
    cursor.execute('SELECT id, name FROM facilities')
    facilities = cursor.fetchall()
    
    print(f"🏢 Found {len(facilities)} facilities")
    
    # Clear existing time slots
    cursor.execute('DELETE FROM time_slots')
    print("🗑️ Cleared existing time slots")
    
    # Add time slots for each facility
    for facility_id, facility_name in facilities:
        print(f"\n📅 Adding time slots for {facility_name} (ID: {facility_id})")
        
        for start_time, end_time, duration in default_slots:
            cursor.execute('''
                INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes)
                VALUES (?, ?, ?, ?)
            ''', (facility_id, start_time, end_time, duration))
            
            print(f"  ✅ {start_time} - {end_time} ({duration} min)")
    
    conn.commit()
    
    # Verify
    cursor.execute('SELECT COUNT(*) FROM time_slots')
    total_slots = cursor.fetchone()[0]
    print(f"\n📊 Total time slots created: {total_slots}")
    
    conn.close()
    print("✅ Time slots setup complete!")

if __name__ == "__main__":
    setup_time_slots()
