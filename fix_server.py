#!/usr/bin/env python3
"""
Fix server encoding issues
"""

with open('server/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic section and replace it
lines = content.split('\n')

# Find the start of the problematic function
start_idx = None
for i, line in enumerate(lines):
    if '@app.route(\'/api/users/profile\', methods=[\'PUT\', \'GET\'])' in line:
        start_idx = i
        break

if start_idx:
    # Find the end of the function (next @app.route or end of file)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip().startswith('@app.route'):
            end_idx = i
            break
        elif i == len(lines) - 1:
            end_idx = len(lines)
    
    # Replace the problematic section
    clean_function = """@app.route('/api/users/profile', methods=['PUT', 'GET'])
def update_user_profile():
    try:
        if request.method == 'GET':
            # Handle GET request for profile retrieval
            # Use email parameter like the existing /api/me endpoint
            email = request.args.get('email')
            if not email:
                return jsonify({'success': False, 'message': 'Email parameter required'}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, email, full_name, role, verified, verification_type, discount_rate, contact_number, address, profile_photo_url, is_active, email_verified, last_login, created_at, updated_at FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            # Convert to dictionary with proper keys
            user_data = {
                'id': user[0],
                'fullName': user[2],
                'email': user[1],
                'contactNumber': user[6],
                'address': user[7],
                'profile_photo_url': user[8],
                'isVerified': user[3],
                'verificationStatus': user[4],
                'createdAt': user[11]
            }
            
            return jsonify({'success': True, 'data': user_data})
        
        elif request.method == 'PUT':
            # Handle PUT request for profile update
            data = request.get_json()
            
            if not data:
                return jsonify({'success': False, 'message': 'No data provided'}), 400
            
            # Get current user data to preserve email
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE id = ?", (data.get('id'),))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            email = result[0]
            
            cursor.execute("""
                UPDATE users 
                SET full_name = ?, contact_number = ?, address = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (
                    data.get('full_name', ''),
                    data.get('contact_number', ''),
                    data.get('address', ''),
                    data.get('id')
                ))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        else:
            return jsonify({'success': False, 'message': 'Method not allowed'}), 405

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500"""
    
    # Replace the lines
    new_lines = lines[:start_idx] + clean_function.split('\n') + lines[end_idx:]
    
    # Write back to file
    with open('server/server.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Server file fixed!")
