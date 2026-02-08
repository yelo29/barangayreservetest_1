import sqlite3

def check_table_schema():
    """Check the schema of the bookings table"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== BOOKINGS TABLE SCHEMA ===")
    cursor.execute('PRAGMA table_info(bookings)')
    columns = cursor.fetchall()
    
    for col in columns:
        print(f"Column {col[0]}: {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_table_schema()
