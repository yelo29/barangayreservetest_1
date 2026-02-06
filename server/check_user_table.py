import sqlite3

def check_user_table():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Check user table structure
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    
    print('Users Table Structure:')
    print('=' * 50)
    for col in columns:
        print(f'{col[1]}: {col[2]}')
    
    # Check current user data
    cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate FROM users ORDER BY id')
    users = cursor.fetchall()
    
    print('\nCurrent Users:')
    print('=' * 50)
    for user in users:
        user_id, email, full_name, verified, verification_type, discount_rate = user
        print(f'ID: {user_id}, Email: {email}, Name: {full_name}')
        print(f'  Verified: {verified}, Type: {verification_type}, Discount: {discount_rate}')
        print('-' * 30)
    
    conn.close()

if __name__ == '__main__':
    check_user_table()
