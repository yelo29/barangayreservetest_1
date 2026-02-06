import sqlite3

def check_receipts():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Check recent bookings with receipt data
    cursor.execute('''
        SELECT id, booking_reference, receipt_base64, receipt_filename, created_at 
        FROM bookings 
        ORDER BY id DESC 
        LIMIT 10
    ''')
    
    rows = cursor.fetchall()
    
    print('Recent Bookings Receipt Check:')
    print('=' * 50)
    
    for row in rows:
        booking_id, booking_ref, receipt_base64, receipt_filename, created_at = row
        has_receipt = receipt_base64 is not None and receipt_base64 != ''
        
        print(f'ID: {booking_id}')
        print(f'Reference: {booking_ref}')
        print(f'Has Receipt: {has_receipt}')
        print(f'Receipt Length: {len(receipt_base64) if receipt_base64 else 0}')
        print(f'Filename: {receipt_filename}')
        print(f'Created: {created_at}')
        print('-' * 30)
    
    # Also check the table structure
    cursor.execute('PRAGMA table_info(bookings)')
    columns = cursor.fetchall()
    
    print('\nBookings Table Structure:')
    print('=' * 50)
    for col in columns:
        print(f'{col[1]}: {col[2]}')
    
    conn.close()

if __name__ == '__main__':
    check_receipts()
