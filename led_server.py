from flask import Flask, render_template
import RPi.GPIO as GPIO         # Import Raspberry Pi GPIO library
from time import sleep          # Import the sleep function 
import time
import board
import neopixel


# Configure the system variables
PIXEL_PIN = board.D18       # GPIO pin used
NUM_PIXELS = 50             # Number of NeoPixels in your strip
BRIGHTNESS = 0.7            # Set brightness level (0.0 to 1.0)

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=BRIGHTNESS, 
    auto_write=False
)

# Define custom color tuples (Green, Red, Blue)
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (0, 255, 127)
CLEAR = (0, 0, 0)

def hsv_to_grb(h, s, v):
    # Chroma, and matching variables based on HSV math
    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c

    # Determine sector on the hue hexagon
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else: # 300 <= h < 360
        r, g, b = c, 0, x

    # Add match value m and scale to 8-bit [0, 255]
    return (
        int((g + m) * 255),
        int((r + m) * 255),
        int((b + m) * 255)
    )



print("Starting stuff")

# Example Usage:
# Hue = 200, Saturation = 0.8, Value = 0.9
# print(hsv_to_rgb(200, 0.8, 0.9))
# Output: (45, 183, 229)


# try:
#     while True:
#         pixels.fill(CLEAR)
#         print("PINK")
#         for i in range(NUM_PIXELS):
#             pixels[i] = hsv_to_grb(7 * i, 1, 0.6)
#             pixels.show()
#             time.sleep(0.1)
#         # 1. Fill the entire strip Blue
#         print("BLUE")
#         for i in range(NUM_PIXELS):
#            pixels[i] = BLUE
#            pixels.show()
#            time.sleep(0.1)
#         pixels.show()
#         time.sleep(1)

#         # 2. Change individual pixels sequentially
#         print("RED")
#         pixels.fill(CLEAR)
#         for i in range(NUM_PIXELS):
#            pixels[i] = RED
#            pixels.show()
#            time.sleep(0.05)
#         time.sleep(1)

#         # 3. Fill the entire strip Green
#         print("GREEN")
#         pixels.fill(GREEN)
#         pixels.show()
#         time.sleep(1)

# except KeyboardInterrupt:
#     # Clean up and turn off LEDs on exit
#     pixels.fill(CLEAR)
#     pixels.show()

# Initialize the Flask application
app = Flask(__name__)

led_status = 0

# Define the root route
@app.route("/")
def home():
    return render_template("index.html")

# Define an additional API route
@app.route("/leds/red/")
def red():
    global pixels
    pixels.fill(RED)
    pixels.show()
    print("Changed pixels to red")
    return "RED"

@app.route("/leds/green/")
def green():
    global pixels
    pixels.fill(GREEN)
    pixels.show()
    print("Changed pixels to green")
    return "GREEN"

@app.route("/leds/blue/")
def blue():
    global pixels
    pixels.fill(BLUE)
    pixels.show()
    print("Changed pixels to blue")
    return "BLUE"
# Start the server if the script is executed directly
if __name__ == "__main__":
    # debug=True enables auto-reload on code changes
    # host="0.0.0.0" allows external access on your local network
    app.run(host="0.0.0.0", port=5000, debug=True)
