from flask import Flask, render_template
import RPi.GPIO as GPIO         # Import Raspberry Pi GPIO library
from time import sleep          # Import the sleep function 

pinLED = 4                      # LED GPIO Pin LED

GPIO.setmode(GPIO.BCM)          # Use GPIO pin number
GPIO.setwarnings(False)         # Ignore warnings in our case
GPIO.setup(pinLED, GPIO.OUT)    # GPIO pin as output pin
# Initialize the Flask application
app = Flask(__name__)

led_status = 0

# Define the root route
@app.route("/")
def home():
    return render_template("index.html")

# Define an additional API route
@app.route("/led/toggle/")
def status():
    global led_status
    if led_status:
        GPIO.output(pinLED, GPIO.LOW)
        led_status = 0
    else:
        GPIO.output(pinLED, GPIO.HIGH)
        led_status = 1
    print("Attempted to Toggle")
    return "Toggled!"

# Start the server if the script is executed directly
if __name__ == "__main__":
    # debug=True enables auto-reload on code changes
    # host="0.0.0.0" allows external access on your local network
    app.run(host="0.0.0.0", port=5000, debug=True)
