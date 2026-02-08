import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== TIME SLOTS DETAILED ===')
cursor.execute('SELECT * FROM time_slots ORDER BY facility_id, start_time')
slots = cursor.fetchall()
print(f'Total time slots: {len(slots)}')
for slot in slots:
    print(f'ID: {slot[0]}, Facility ID: {slot[1]}, Start: {slot[2]}, End: {slot[3]}')

print('\n=== TIME SLOTS BY FACILITY ===')
for facility_id in range(1, 5):
    cursor.execute('SELECT start_time, end_time FROM time_slots WHERE facility_id = ? ORDER BY start_time', (facility_id,))
    facility_slots = cursor.fetchall()
    print(f'Facility {facility_id}: {len(facility_slots)} time slots')
    for slot in facility_slots[:3]:  # Show first 3 only
        print(f'  {slot[0]} - {slot[1]}')
    if len(facility_slots) > 3:
        print(f'  ... and {len(facility_slots) - 3} more')

conn.close()
