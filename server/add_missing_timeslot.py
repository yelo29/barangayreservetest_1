import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('=== ADDING MISSING 6:00 AM - 8:00 AM TIME SLOT ===')

# Add the missing 6:00 AM - 8:00 AM time slot for Community Hall
cursor.execute('''
    INSERT INTO time_slots (facility_id, start_time, end_time, duration_minutes)
    VALUES (?, ?, ?, ?)
''', (
    1,  # Community Hall facility_id
    '6:00 AM',  # start_time
    '8:00 AM',  # end_time
    120  # duration_minutes (2 hours)
))

conn.commit()
conn.close()

print('✅ Added missing 6:00 AM - 8:00 AM time slot for Community Hall')

# Verify the addition
conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

print('\n=== UPDATED TIME SLOTS FOR COMMUNITY HALL ===')
cursor.execute('SELECT id, start_time, end_time FROM time_slots WHERE facility_id = 1 ORDER BY start_time')
slots = cursor.fetchall()
for slot in slots:
    print(f'ID: {slot[0]}, Time: {slot[1]} - {slot[2]}')

conn.close()

print('\n🎯 The 6:00 AM - 8:00 AM time slot is now available!')
print('📱 The official booking form should now show the resident booking for this time slot.')
