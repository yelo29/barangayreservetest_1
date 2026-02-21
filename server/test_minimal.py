from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users/profile', methods=['PUT', 'GET'])
def update_user_profile():
    try:
        if request.method == 'GET':
            email = request.args.get('email')
            return jsonify({'success': True, 'message': f'GET request for email: {email}'})
        
        elif request.method == 'PUT':
            data = request.get_json()
            return jsonify({'success': True, 'message': f'PUT request with data: {data}'})
        
        else:
            return jsonify({'success': False, 'message': 'Method not allowed'}), 405
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
