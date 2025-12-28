from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Current status storage
current_status = "available"

# This part sends the HTML file to your iPhone browser
@app.route('/')
def index():
    # Looks for index.html in the same folder as this script
    return send_from_directory('.', 'index.html')

@app.route('/set_led', methods=['POST'])
def set_status():
    global current_status
    data = request.json
    current_status = data.get('status')
    print(f">>> Status Updated to: {current_status}")
    return jsonify({"success": True})

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"state": current_status})

if __name__ == '__main__':
    print("========================================")
    print("STATUS HUB SERVER IS STARTING")
    print("PC Access: http://localhost:8080")
    print("iPhone Access: http://10.0.0.151:8080")
    print("========================================")
    
    # Using Port 8080 because Port 5000 is often blocked on Windows
    app.run(host='0.0.0.0', port=8080)
