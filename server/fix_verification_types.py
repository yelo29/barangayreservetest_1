import sqlite3
from datetime import datetime

def fix_verification_types():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Update users based on their current verified status
    print("Fixing verification types for existing users...")
    
    # For users with verified = 1, set verification_type = 'resident'
    cursor.execute('''
        UPDATE users 
        SET verification_type = 'resident', updated_at = ?
        WHERE verified = 1 AND verification_type IS NULL
    ''', (datetime.now(),))
    
    # For users with verified = 2, set verification_type = 'non-resident'  
    cursor.execute('''
        UPDATE users 
        SET verification_type = 'non-resident', updated_at = ?
        WHERE verified = 2 AND verification_type IS NULL
    ''', (datetime.now(),))
    
    # For users with verified = 0, set verification_type = NULL
    cursor.execute('''
        UPDATE users 
        SET verification_type = NULL, updated_at = ?
        WHERE verified = 0 AND verification_type IS NULL
    ''', (datetime.now(),))
    
    conn.commit()
    
    # Check results
    cursor.execute('SELECT id, email, full_name, verified, verification_type, discount_rate FROM users ORDER BY id')
    users = cursor.fetchall()
    
    print('Updated Users:')
    print('=' * 50)
    for user in users:
        user_id, email, full_name, verified, verification_type, discount_rate = user
        print(f'ID: {user_id}, Email: {email}')
        print(f'  Verified: {verified}, Type: {verification_type}, Discount: {discount_rate}')
        print('-' * 30)
    
    conn.close()
    print("✅ Verification types fixed!")

if __name__ == '__main__':
    fix_verification_types()
