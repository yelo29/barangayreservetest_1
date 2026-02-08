#!/usr/bin/env python3
import sqlite3

def debug_dict_creation():
    conn = sqlite3.connect('barangay.db')
    cursor = conn.cursor()
    
    # Get column names from bookings table
    cursor.execute('PRAGMA table_info(bookings)')
    booking_columns = [col[1] for col in cursor.fetchall()]
    print(f'Bookings columns: {booking_columns[:10]}...')  # First 10 columns
    
    # Get column names from query result
    cursor.execute('''
        SELECT b.id, b.booking_reference, b.user_id, b.facility_id, b.time_slot_id, 
               b.booking_date, b.start_time, b.end_time, b.duration_hours,
               b.purpose, b.expected_attendees, b.special_requirements,
               b.contact_number, b.contact_address, b.base_rate, b.discount_rate,
               b.discount_amount, b.downpayment_amount, b.total_amount,
               b.receipt_base64, b.receipt_filename, b.receipt_uploaded_at,
               b.status, b.priority_level, b.approved_by, b.approved_at,
               b.rejection_reason, b.is_competitive, b.competing_booking_ids,
               b.competition_resolved, b.created_at, b.updated_at,
               f.name as facility_name, u.full_name, u.email as user_email, u.verified, u.discount_rate, u.role as user_role
        FROM bookings b
        LEFT JOIN facilities f ON b.facility_id = f.id
        LEFT JOIN users u ON b.user_id = u.id
        ORDER BY b.booking_date DESC, b.start_time ASC
        LIMIT 1
    ''')
    
    # Get column names from the query
    cursor.execute('PRAGMA table_info(temp.bookings_query)')
    try:
        temp_columns = [col[1] for col in cursor.fetchall()]
        print(f'Query columns: {temp_columns[:10]}...')  # First 10 columns
    except:
        print('No temp table created')
    
    # Get actual booking
    booking = cursor.fetchone()
    if booking:
        print(f'\nSample booking tuple length: {len(booking)}')
        
        # Create dict manually to see mapping
        column_names = [
            'id', 'booking_reference', 'user_id', 'facility_id', 'time_slot_id',
            'booking_date', 'start_time', 'end_time', 'duration_hours',
            'purpose', 'expected_attendees', 'special_requirements',
            'contact_number', 'contact_address', 'base_rate', 'discount_rate',
            'discount_amount', 'downpayment_amount', 'total_amount',
            'receipt_base64', 'receipt_filename', 'receipt_uploaded_at',
            'status', 'priority_level', 'approved_by', 'approved_at',
            'rejection_reason', 'is_competitive', 'competing_booking_ids',
            'competition_resolved', 'created_at', 'updated_at',
            'facility_name', 'user_email', 'verified', 'discount_rate', 'user_role'
        ]
        
        booking_dict = {}
        for i, col_name in enumerate(column_names):
            if i < len(booking):
                booking_dict[col_name] = booking[i]
        
        print(f'Created dict keys: {list(booking_dict.keys())[:10]}...')
        print(f'Key values: booking_date={booking_dict.get("booking_date")}, user_role={booking_dict.get("user_role")}, status={booking_dict.get("status")}')
    
    conn.close()

if __name__ == '__main__':
    debug_dict_creation()
