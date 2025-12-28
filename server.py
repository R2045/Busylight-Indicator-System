from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app) 

# --- GLOBAL STATE ---
# This keeps track of your status so all connected devices stay in sync
current_status = {
    "state": "available",
    "last_updated": ""
}
lock = threading.Lock()

@app.route('/set_led', methods=['POST'])
def set_status():
    """Updates the global status from any controller device."""
    global current_status
    data = request.json
    status = data.get('status')
    
    valid_statuses = ["available", "busy-talkable", "dnd", "off"]
    
    if status in valid_statuses:
        with lock:
            current_status["state"] = status
        print(f"Status changed to: {status}")
        return jsonify({"success": True, "status": status})
    
    return jsonify({"success": False, "error": "Invalid status"}), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    """Any device calls this to see what color it should be showing."""
    with lock:
        return jsonify(current_status)

if __name__ == '__main__':
    print("--- Universal Status Hub Started ---")
    print("Point your browser(s) to this machine's IP address on port 5000")
    # host='0.0.0.0' allows other devices on your Wi-Fi to connect
    app.run(host='0.0.0.0', port=5000)
