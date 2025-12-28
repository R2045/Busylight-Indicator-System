from flask import send_from_directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html');
    
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app) # This allows different devices to talk to the server
CORS(app)

# --- GLOBAL STATE ---
current_status = {"state": "available"}
lock = threading.Lock()
# Global status
current_status = "available"

@app.route('/set_led', methods=['POST'])
def set_status():
    """Updates the global status from any device."""
global current_status
data = request.json
    status = data.get('status')
    new_state = data.get('status')

    valid_statuses = ["available", "busy-talkable", "dnd"]
    # This will print in your command prompt so you can see the click happen
    print(f">>> Button Clicked! Changing state to: {new_state}")

    if status in valid_statuses:
        with lock:
            current_status["state"] = status
        print(f"Status changed to: {status}")
        return jsonify({"success": True, "status": status})
    
    return jsonify({"success": False, "error": "Invalid status"}), 400
    current_status = new_state
    return jsonify({"success": True, "state": current_status})

@app.route('/get_status', methods=['GET'])
def get_status():
    """Devices call this to see what color to display."""
    with lock:
        return jsonify(current_status)
    return jsonify({"state": current_status})

if __name__ == '__main__':
    print("--- Universal Status Hub Started ---")
    print("Point your browsers to http://10.0.0.151:5000")
    # host='0.0.0.0' makes it accessible on your Wi-Fi network
    app.run(host='0.0.0.0', port=5000)
    # Running on your specific IP
    app.run(host='0.0.0.0', port=5000, debug=False)
