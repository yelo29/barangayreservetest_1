# 🔧 SERVER IMPLEMENTATION GUIDE

## 📊 CURRENT SERVER STATUS (from tests):
- ❌ Profile Photo Upload: 404 (Not Found)
- ❌ Profile Update: 500 (Internal Error - missing 'email' field)
- ⚠️ Profile Retrieval: 405 (Method Not Allowed - GET not supported)

## 🛠️ ISSUES IDENTIFIED:

### 1. Profile Photo Upload Endpoint Missing
- **Error**: 404 Not Found
- **Solution**: Implement `/api/users/profile-photo` POST endpoint
- **Priority**: HIGH

### 2. Profile Update Endpoint Has Server Error
- **Error**: 500 Internal Server Error
- **Message**: `'email'` field missing
- **Solution**: Fix the profile update logic
- **Priority**: HIGH

### 3. Profile Retrieval Method Not Supported
- **Error**: 405 Method Not Allowed
- **Solution**: Add GET method support or fix method routing
- **Priority**: MEDIUM

## 🎯 STEP-BY-STEP IMPLEMENTATION:

### STEP 1: Add Required Imports and Configuration
```python
import os
import uuid
from werkzeug.utils import secure_filename
from functools import wraps

# Add to Flask app configuration
app.config['UPLOAD_FOLDER'] = 'uploads/profile_photos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
```

### STEP 2: Create Helper Functions
```python
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename_custom(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return f"{uuid.uuid4().hex}.{ext}"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            # Decode token and get user identity
            user_id = decode_jwt(token)
            if user_id:
                g.current_user_id = user_id
                return f(*args, **kwargs)
            else:
                return jsonify({'success': False, 'message': 'Invalid token'}), 401
        except:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
    return decorated_function

def get_jwt_identity():
    return getattr(g, 'current_user_id', None)

def decode_jwt(token):
    # Implement JWT decoding logic here
    # Return user_id if valid, None if invalid
    pass
```

### STEP 3: Implement Profile Photo Upload Endpoint
```python
@app.route('/api/users/profile-photo', methods=['POST'])
@jwt_required
def upload_profile_photo():
    try:
        if 'profile_photo' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['profile_photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type'}), 400
        
        filename = secure_filename_custom(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET profile_photo_url = ? WHERE id = ?", (filename, user_id))
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
```

### STEP 4: Fix Profile Update Endpoint
```python
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
        
        # Get current user data to preserve email
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        email = result[0]
        
        # Update profile (email is preserved)
        cursor.execute("""
            UPDATE users 
            SET full_name = ?, contact_number = ?, address = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            data.get('fullName', ''),
            data.get('contactNumber', ''),
            data.get('address', ''),
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
```

### STEP 5: Add Profile Retrieval Endpoint
```python
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
            SELECT id, full_name, email, contact_number, address, 
                   profile_photo_url, is_verified, verification_status
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user_data = {
            'id': user[0],
            'fullName': user[1],
            'email': user[2],
            'contactNumber': user[3],
            'address': user[4],
            'profile_photo_url': user[5],
            'isVerified': user[6],
            'verificationStatus': user[7]
        }
        
        return jsonify({'success': True, 'data': user_data})
        
    except Exception as e:
        print(f"Error getting profile: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500
```

## 🧪 TESTING AFTER IMPLEMENTATION:

1. **Add endpoints to your Flask app.py**
2. **Run the test script**: `python test_server_fix.py`
3. **Verify all endpoints return 200 status**
4. **Test in Flutter app**

## 🎯 EXPECTED RESULTS AFTER FIX:
- ✅ Profile Photo Upload: 200 (working)
- ✅ Profile Update: 200 (working)
- ✅ Profile Retrieval: 200 (working)
- 🎉 All Flutter app features working perfectly!

## 📋 CROSS-IMPLICATIONS TO CONSIDER:

### Client-Side:
- ✅ Already implemented and working
- ✅ Error handling in place
- ✅ Will work immediately after server fix

### Server-Side:
- 🔧 Need to implement missing endpoints
- 🔧 Need proper error handling
- 🔧 Need file upload handling
- 🔧 Need JWT authentication middleware

## 🚀 FINAL RECOMMENDATION:

**Implement the server endpoints step by step, testing each one as you go. This approach ensures:**
1. **Incremental progress** - Each endpoint tested individually
2. **Early error detection** - Issues caught immediately
3. **Cross-implication awareness** - Client and server tested together
4. **Robust solution** - Full end-to-end functionality
