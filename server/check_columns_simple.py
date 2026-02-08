import sqlite3

try:
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    cursor.execute('PRAGMA table_info(bookings)')
    columns = cursor.fetchall()
    
    print('Bookings table columns:')
    for col in columns:
        print(f'{col[1]} ({col[2]})')
    
    # Check if rejection_reason column exists
    cursor.execute("SELECT COUNT(*) FROM pragma_table_info('bookings') WHERE name = 'rejection_reason'")
    rejection_reason_exists = cursor.fetchone()[0]
    print(f'\nrejection_reason column exists: {rejection_reason_exists > 0}')
    
    conn.close()
except Exception as e:
    print(f'Error: {e}')
