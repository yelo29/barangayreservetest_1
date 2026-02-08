import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Regenerate time slots for all facilities
facilities = cursor.execute('SELECT id, name FROM facilities').fetchall()
print(f'🔄 Regenerating time slots for {len(facilities)} facilities...')

for facility in facilities:
    facility_id, facility_name = facility
    print(f'Processing facility {facility_id}: {facility_name}')
    
    # Delete existing time slots
    cursor.execute('DELETE FROM time_slots WHERE facility_id = ?', (facility_id,))
    
    # Generate 2-hour time slots
    facility_name_lower = facility_name.lower()
    if 'basketball' in facility_name_lower or 'court' in facility_name_lower:
        start_hour, end_hour = 6, 22  # 6 AM to 9 PM
    elif 'swimming' in facility_name_lower or 'pool' in facility_name_lower:
        start_hour, end_hour = 6, 21  # 6 AM to 8 PM
    elif 'shooting' in facility_name_lower or 'range' in facility_name_lower:
        start_hour, end_hour = 8, 18  # 8 AM to 5 PM
    else:
        start_hour, end_hour = 8, 21  # Default 8 AM to 8 PM
    
    # Generate 2-hour slots
    time_slots = []
    for hour in range(start_hour, end_hour, 2):
        start_time = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
        end_time = f"{(hour + 2) % 12 or 12}:00 {'AM' if hour + 2 < 12 else 'PM'}"
        duration_minutes = 120  # 2 hours
        time_slots.append((facility_id, start_time, end_time, duration_minutes))
    
    # Insert time slots
    cursor.executemany('INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes) VALUES (?, ?, ?, ?)', time_slots)
    print(f'  Created {len(time_slots)} time slots')

conn.commit()
conn.close()
print('✅ Time slots regeneration complete!')
