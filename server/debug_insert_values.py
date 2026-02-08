# Debug the INSERT statement values
from datetime import datetime

values = [
    f'BKG-{datetime.now().strftime("%Y%m%d%H%M%S")}',  # 1: booking_reference
    1,  # 2: user_id
    1,  # 3: facility_id
    163,  # 4: time_slot_id
    '2026-02-18',  # 5: booking_date
    '6:00 AM',  # 6: start_time
    '8:00 AM',  # 7: end_time
    2.0,  # 8: duration_hours
    'Official barangay meeting',  # 9: purpose
    10,  # 10: expected_attendees
    None,  # 11: special_requirements
    None,  # 12: contact_number
    None,  # 13: contact_address
    1000.0,  # 14: base_rate
    0.00,  # 15: discount_rate
    0.00,  # 16: discount_amount
    200.0,  # 17: downpayment_amount
    1000.0,  # 18: total_amount
    'pending',  # 19: status
    datetime.now().isoformat()  # 20: created_at
]

print(f'Total values: {len(values)}')
for i, value in enumerate(values):
    print(f'{i+1}: {value}')
