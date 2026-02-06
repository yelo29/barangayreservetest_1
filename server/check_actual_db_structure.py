#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('barangay.db')
cursor = conn.cursor()

# Get the actual table structure
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("Actual users table structure:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
