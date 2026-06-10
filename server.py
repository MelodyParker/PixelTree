from flask import Flask, render_template
from gpiozero import LED

# Initialize the Flask application
app = Flask(__name__)

led = LED(17)
led_status = 0

# Define the root route
@app.route("/")
def home():
    return render_template("index.html")

# Define an additional API route
@app.route("/led/toggle")
def status():
    global led_status
    if led_status:
        led.off()
        led_status = 0
    else:
        led.on()
        led_status = 1
    return "Toggled!"

# Start the server if the script is executed directly
if __name__ == "__main__":
    # debug=True enables auto-reload on code changes
    # host="0.0.0.0" allows external access on your local network
    app.run(host="0.0.0.0", port=80, debug=True)
