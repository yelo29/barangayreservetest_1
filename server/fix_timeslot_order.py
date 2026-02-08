import sqlite3

def fix_time_slot_order():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('=== FIXING TIME SLOT ORDER ===')
    
    # Get all time slots for Community Hall
    cursor.execute('SELECT id, start_time, end_time FROM time_slots WHERE facility_id = 1')
    slots = cursor.fetchall()
    
    # Function to convert time to minutes for proper sorting
    def time_to_minutes(time_str):
        """Convert time string like '6:00 AM' to minutes from midnight"""
        if 'AM' in time_str:
            parts = time_str.replace(' AM', '').split(':')
            hour = int(parts[0])
            minute = int(parts[1])
            if hour == 12:  # 12 AM is midnight
                hour = 0
            return hour * 60 + minute
        elif 'PM' in time_str:
            parts = time_str.replace(' PM', '').split(':')
            hour = int(parts[0])
            minute = int(parts[1])
            if hour != 12:  # 12 PM stays 12, other PM hours add 12
                hour += 12
            return hour * 60 + minute
        return 0
    
    # Sort slots chronologically
    sorted_slots = sorted(slots, key=lambda x: time_to_minutes(x[1]))
    
    print('\n=== CHRONOLOGICAL ORDER ===')
    for slot in sorted_slots:
        print(f'ID: {slot[0]}, Time: {slot[1]} - {slot[2]}')
    
    # Update the database with proper sorting by creating a sort_order column
    try:
        cursor.execute('ALTER TABLE time_slots ADD COLUMN sort_order INTEGER')
        print('\n✅ Added sort_order column')
    except:
        print('\n📝 sort_order column already exists')
    
    # Update sort_order for each slot
    for i, slot in enumerate(sorted_slots):
        cursor.execute('UPDATE time_slots SET sort_order = ? WHERE id = ?', (i + 1, slot[0]))
    
    conn.commit()
    conn.close()
    
    print('\n✅ Time slot order fixed!')
    print('🎯 6:00 AM - 8:00 AM should now appear first in the list')

if __name__ == '__main__':
    fix_time_slot_order()
