from flask import Flask
from gpiozero import LED

# Initialize the Flask application
app = Flask(__name__)

led = LED(17)
led_status = 0

# Define the root route
@app.route("/")
def home():
    return "<h1>Flask Server is Running!</h1>"

# Define an additional API route
@app.route("/api/toggle")
def status():
    if led_status:
        led.off()
        led_status = 0
    else:
        led.on()
        led_status = 1
    return "Bob"

# Start the server if the script is executed directly
if __name__ == "__main__":
    # debug=True enables auto-reload on code changes
    # host="0.0.0.0" allows external access on your local network
    app.run(host="0.0.0.0", port=5000, debug=True)
