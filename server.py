from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Global status
current_status = "available"

# --- THE PRO TRICK: This sends the HTML to your iPhone Safari ---
@app.route('/')
def index():
    # Make sure index.html is in the same folder as this script!
    return send_from_directory('.', 'index.html')

@app.route('/set_led', methods=['POST'])
def set_status():
    global current_status
    data = request.json
    current_status = data.get('status')
    print(f"Status changed to: {current_status}")
    return jsonify({"success": True})

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"state": current_status})

if __name__ == '__main__':
    print("--- SERVER STARTING ---")
    print("On your iPhone Safari, type: http://10.0.0.151:5000")
    app.run(host='0.0.0.0', port=5000)
