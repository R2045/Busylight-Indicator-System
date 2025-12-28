from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global status
current_status = "available"

@app.route('/set_led', methods=['POST'])
def set_status():
    global current_status
    data = request.json
    new_state = data.get('status')
    
    # This will print in your command prompt so you can see the click happen
    print(f">>> Button Clicked! Changing state to: {new_state}")
    
    current_status = new_state
    return jsonify({"success": True, "state": current_status})

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"state": current_status})

if __name__ == '__main__':
    # Running on your specific IP
    app.run(host='0.0.0.0', port=5000, debug=False)
