#!/usr/bin/env python3
import sqlite3

def test_officials():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, full_name, contact_number, role, email FROM users WHERE role = "official" ORDER BY full_name')
    officials = cursor.fetchall()
    
    print('📋 Current officials in database:')
    for official in officials:
        print(f'  {official[0]}: {official[1]} - {official[4]} - Contact: {official[2] or "None"}')
    
    conn.close()

if __name__ == "__main__":
    test_officials()
