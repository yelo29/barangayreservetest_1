"""
Missing server endpoints for profile updates
Add these to your Flask server (app.py)
"""

# 1. PROFILE PHOTO UPLOAD ENDPOINT
@app.route('/api/users/profile-photo', methods=['POST'])
@jwt_required
def upload_profile_photo():
    try:
        # Check if file was uploaded
        if 'profile_photo' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['profile_photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type. Only JPG, PNG, GIF allowed.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Get current user
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Update user's profile photo URL in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET profile_photo_url = ? WHERE id = ?
        """, (filename, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'photo_url': filename,
            'message': 'Profile photo uploaded successfully'
        })
        
    except Exception as e:
        print(f"Error uploading profile photo: {e}")
        return jsonify({'success': False, 'message': 'Server error during upload'}), 500

# 2. PROFILE UPDATE ENDPOINT (FIXED)
@app.route('/api/users/profile', methods=['PUT'])
@jwt_required
def update_user_profile():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['fullName', 'contactNumber', 'address']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Update user profile
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET full_name = ?, contact_number = ?, address = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            data['fullName'],
            data['contactNumber'], 
            data['address'],
            user_id
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        })
        
    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'success': False, 'message': 'Server error during update'}), 500

# 3. PROFILE GET ENDPOINT (FOR AUTO-FILL)
@app.route('/api/users/profile', methods=['GET'])
@jwt_required
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, full_name, email, contact_number, address, profile_photo_url, 
                   is_verified, verification_status, created_at
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Convert to dictionary with proper keys
        user_data = {
            'id': user[0],
            'fullName': user[1],
            'email': user[2],
            'contactNumber': user[3],
            'address': user[4],
            'profile_photo_url': user[5],
            'isVerified': user[6],
            'verificationStatus': user[7],
            'createdAt': user[8]
        }
        
        return jsonify({'success': True, 'data': user_data})
        
    except Exception as e:
        print(f"Error getting profile: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

# 4. HELPER FUNCTIONS
def allowed_file(filename):
    """Check if file type is allowed"""
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """Generate secure filename"""
    import uuid
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return f"{uuid.uuid4().hex}.{ext}"

# 5. CONFIGURATION UPDATES NEEDED
"""
Add to your Flask app configuration:

import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'uploads/profile_photos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
"""

print("""
📋 SERVER ENDPOINTS CREATED!
📁 Copy the code above into your Flask app.py
🔧 Make sure you have these imports:
   - from werkzeug.utils import secure_filename
   - import os
   - import uuid

🎯 ENDPOINTS INCLUDED:
   ✅ POST /api/users/profile-photo (file upload)
   ✅ PUT /api/users/profile (profile update)  
   ✅ GET /api/users/profile (profile retrieval)

📋 NEXT STEPS:
   1. Add the endpoints to your Flask app
   2. Test with the simple_test.py script
   3. Verify all endpoints work correctly
   4. Test in the Flutter app
""")
