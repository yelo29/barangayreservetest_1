import sqlite3

def test_gym_regeneration():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('=== TESTING GYM TIME SLOT REGENERATION ===')
    
    # Clear existing time slots for Gym
    cursor.execute('DELETE FROM time_slots WHERE facility_id = 6')
    print('🗑️ Cleared existing Gym time slots')
    
    # Generate time slots manually (same as regenerate function)
    facility_id = 6
    facility_name = 'Gym'
    start_hour, end_hour = 6, 21  # Default 6 AM to 8 PM
    
    time_slots = []
    for i, hour in enumerate(range(start_hour, end_hour, 2)):  # Increment by 2 hours
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 2) % 12 or 12}:00 {'AM' if hour + 2 < 12 else 'PM'}"
        duration_minutes = 120  # 2 hour slots
        sort_order = i + 1  # Chronological order
        time_slots.append((facility_id, start_time, end_time, duration_minutes, sort_order))
        print(f'📝 Slot {i+1}: {start_time} - {end_time} (sort_order: {sort_order})')
    
    # Insert time slots with explicit column names
    cursor.executemany('''
        INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes, sort_order)
        VALUES (?, ?, ?, ?, ?)
    ''', time_slots)
    
    conn.commit()
    
    # Verify insertion
    cursor.execute('SELECT id, start_time, end_time, sort_order FROM time_slots WHERE facility_id = 6 ORDER BY sort_order')
    slots = cursor.fetchall()
    
    print('\n=== VERIFICATION ===')
    for slot in slots:
        print(f'ID: {slot[0]}, Time: {slot[1]} - {slot[2]}, Sort: {slot[3]}')
    
    conn.close()
    print(f'\n✅ Gym time slots regenerated: {len(slots)} slots')

if __name__ == '__main__':
    test_gym_regeneration()
