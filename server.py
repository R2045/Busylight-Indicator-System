from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

current_status = "available"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/set_led', methods=['POST'])
def set_status():
    global current_status
    data = request.json
    current_status = data.get('status')
    print(f"Update received: {current_status}")
    return jsonify({"success": True})

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"state": current_status})

if __name__ == '__main__':
    print("--- SERVER IS LIVE ---")
    print("If on Hotspot, use: http://192.168.137.1:8080")
    app.run(host='0.0.0.0', port=8080)
