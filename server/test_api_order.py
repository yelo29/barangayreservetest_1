import sqlite3

def test_database_order():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print('=== TESTING DATABASE ORDER ===')
    
    # Test the exact query used in API
    cursor.execute('''
        SELECT start_time, end_time FROM time_slots 
        WHERE facility_id = ? 
        ORDER BY sort_order
    ''', (1,))
    
    slots = cursor.fetchall()
    
    print('\nDatabase query results:')
    for i, slot in enumerate(slots):
        print(f'{i+1}: {slot[0]} - {slot[1]}')
    
    conn.close()

if __name__ == '__main__':
    test_database_order()
