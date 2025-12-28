from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app) 

# Current State Storage
current_status = {"state": "available"}
lock = threading.Lock()

@app.route('/set_led', methods=['POST'])
def set_status():
    global current_status
    status = request.json.get('status')
    if status in ["available", "busy-talkable", "dnd", "off"]:
        with lock:
            current_status["state"] = status
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    with lock:
        return jsonify(current_status)

if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible to your other devices on Wi-Fi
    app.run(host='0.0.0.0', port=5000)
