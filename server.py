from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app) # This allows different devices to talk to the server

# --- GLOBAL STATE ---
current_status = {"state": "available"}
lock = threading.Lock()

@app.route('/set_led', methods=['POST'])
def set_status():
    """Updates the global status from any device."""
    global current_status
    data = request.json
    status = data.get('status')
    
    valid_statuses = ["available", "busy-talkable", "dnd"]
    
    if status in valid_statuses:
        with lock:
            current_status["state"] = status
        print(f"Status changed to: {status}")
        return jsonify({"success": True, "status": status})
    
    return jsonify({"success": False, "error": "Invalid status"}), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    """Devices call this to see what color to display."""
    with lock:
        return jsonify(current_status)

if __name__ == '__main__':
    print("--- Universal Status Hub Started ---")
    print("Point your browsers to http://10.0.0.151:5000")
    # host='0.0.0.0' makes it accessible on your Wi-Fi network
    app.run(host='0.0.0.0', port=5000)
