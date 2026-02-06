import sqlite3

def check_users():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, full_name, role FROM users ORDER BY id')
    users = cursor.fetchall()
    
    print('Available Users:')
    print('=' * 50)
    for user in users:
        print(f'ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}')
    
    conn.close()

if __name__ == '__main__':
    check_users()
