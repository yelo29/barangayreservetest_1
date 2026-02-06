#!/usr/bin/env python3
import sqlite3

def check_database():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()

    print('=== USERS TABLE STRUCTURE ===')
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    for col in columns:
        print(f'{col[1]} - {col[2]}')

    print('\n=== USER DATA FOR GMAIL USERS ===')
    cursor.execute('SELECT email, verified, discount_rate FROM users WHERE email LIKE "%gmail.com%"')
    users = cursor.fetchall()
    for user in users:
        print(f'{user[0]} - verified: {user[1]} - discount_rate: {user[2]}')

    print('\n=== BOOKINGS TABLE STRUCTURE ===')
    cursor.execute('PRAGMA table_info(bookings)')
    columns = cursor.fetchall()
    for col in columns:
        print(f'{col[1]} - {col[2]}')

    print('\n=== RECENT BOOKINGS ===')
    cursor.execute('''
        SELECT u.email as user_email, b.receipt_base64, b.booking_date
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC LIMIT 5
    ''')
    bookings = cursor.fetchall()
    for booking in bookings:
        receipt_status = "HAS RECEIPT" if booking[1] and len(booking[1]) > 0 else "NO RECEIPT"
        print(f'{booking[0]} - {booking[2]} - {receipt_status}')

    conn.close()

if __name__ == '__main__':
    check_database()
