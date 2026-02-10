import sqlite3

def check_users_table_structure():
    """Check users table structure"""
    
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    print("=== USERS TABLE STRUCTURE ===")
    
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    
    print("📋 Columns in users table:")
    for col in columns:
        col_id, name, type_name, not_null, default_val, pk = col
        print(f"  📧 {name}: {type_name}")
    
    conn.close()

if __name__ == "__main__":
    check_users_table_structure()
