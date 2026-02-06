#!/usr/bin/env python3
"""
Database Manager for Barangay Reserve
Handles all database connections with proper locking prevention
"""

import sqlite3
import threading
from contextlib import contextmanager
from config import Config

# Global lock for database access
db_lock = threading.Lock()

class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections with proper locking"""
        conn = None
        try:
            with db_lock:
                conn = sqlite3.connect(self.db_path, timeout=30.0)  # 30 second timeout
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Enable WAL mode for better concurrency
                cursor.execute('PRAGMA journal_mode=WAL')
                cursor.execute('PRAGMA synchronous=NORMAL')
                cursor.execute('PRAGMA cache_size=10000')
                cursor.execute('PRAGMA temp_store=MEMORY')
                
                yield conn, cursor
                
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.commit()
                conn.close()

# Global instance
db_manager = DatabaseManager()

# Convenience functions
def get_db_connection():
    """Get database connection with proper locking"""
    return db_manager.get_connection()

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Execute a query with proper connection management"""
    with get_db_connection() as (conn, cursor):
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return None

def execute_update(query, params=None):
    """Execute an update query with proper connection management"""
    with get_db_connection() as (conn, cursor):
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.rowcount
