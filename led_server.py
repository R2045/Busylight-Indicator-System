import RPi.GPIO as GPIO
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

# --- CONFIGURATION ---
GREEN_LED = 17 
YELLOW_LED = 27
RED_LED = 22  

current_led_state = "available"
lock = threading.Lock()

app = Flask(__name__)
CORS(app) 

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in [GREEN_LED, YELLOW_LED, RED_LED]:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def set_leds(green, yellow, red):
    GPIO.output(GREEN_LED, GPIO.HIGH if green else GPIO.LOW)
    GPIO.output(YELLOW_LED, GPIO.HIGH if yellow else GPIO.LOW)
    GPIO.output(RED_LED, GPIO.HIGH if red else GPIO.LOW)

def led_control_loop():
    global current_led_state
    led_on = True 
    
    while True:
        with lock:
            state = current_led_state
        
        if state == "available":
            # Come on in - Solid Green
            set_leds(True, False, False)
            time.sleep(0.5) # Efficiency sleep
        
        elif state == "busy-talkable":
            # Fast/Mid Blink Yellow
            if led_on:
                set_leds(False, True, False)
            else:
                set_leds(False, False, False)
            led_on = not led_on
            time.sleep(0.2) # Fast pace
            
        elif state == "dnd":
            # Slow Blink Red
            if led_on:
                set_leds(False, False, True)
            else:
                set_leds(False, False, False)
            led_on = not led_on
            time.sleep(0.8) # Slow, steady pace

@app.route('/set_led', methods=['POST'])
def set_led_route():
    global current_led_state
    status = request.json.get('status')
    
    if status in ["available", "busy-talkable", "dnd"]:
        with lock:
            current_led_state = status
        print(f"Status changed to: {status}")
        return jsonify({"success": True, "status": status})
    
    return jsonify({"success": False, "error": "Invalid status"}), 400

if __name__ == '__main__':
    setup_gpio()
    threading.Thread(target=led_control_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
