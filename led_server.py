from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO         # Import Raspberry Pi GPIO library
from time import sleep          # Import the sleep function 
import time
import board
import neopixel
import asyncio
from effects_engine.Effect import Effect
from effects_engine.Effects_Engine import Effects_Engine


# Configure the system variables
PIXEL_PIN = board.D18       # GPIO pin used
NUM_PIXELS = 50             # Number of NeoPixels in your strip
BRIGHTNESS = 0.3            # Set brightness level (0.0 to 1.0)

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

def gamma_correct(color):
    # A standard gamma value for NeoPixels
    gamma_val = 3
    
    # Unpack RGB tuple
    r, g, b = color
    
    # Apply the gamma curve to each channel
    # Normalizing by 255.0, raising to power of gamma, then multiplying by 255
    r_corr = int(pow(r / 255.0, gamma_val) * 255.0)
    g_corr = int(pow(g / 255.0, gamma_val) * 255.0)
    b_corr = int(pow(b / 255.0, gamma_val) * 255.0)
    
    return (r_corr, g_corr, b_corr)


print("Starting stuff")

engine = Effects_Engine(pixels)

@engine.register_effect_factory("off", name="All Off", description="Turns off all LEDs", params=[])
class OffEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((0, 0, 0))
        pixels.show()

@engine.register_effect_factory("fill-red", name="Fill Red", description="Colors all LEDs red", params=[])
class FillRedEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((255, 0, 0))
        pixels.show()

@engine.register_effect_factory("fill-rgb", name="Fill RGB", 
                                description="Colors all LEDs with the specified RGB color",
                                params=[{"type": "color", "name": "Color"}])
class FillRGBEffect(Effect):
    @staticmethod
    async def run(pixels, rgb, *args, **kwargs):
        # r, g, b = rgb
        pixels.fill(gamma_correct(rgb))
        pixels.show()

@engine.register_effect_factory("flash-colors", name="Flash Colors",
                                description="Flashes all pixels with the given colors",
                                params=[{"type": "list color", "length": "N", "name": "Colors"}, 
                                        {"type": "list number", "length": "N", "name": "Durations"}])
class FlashColorsEffect(Effect):
    @staticmethod
    async def run(pixels, colors, durations, *args, **kwargs):
        while True:
            for color, duration in zip(colors, durations):
                # r, g, b = color
                pixels.fill(color)
                pixels.show()
                await asyncio.sleep(duration)

@engine.register_effect_factory("alternating-colors", name="Alternate Colors",
                                description="Alternates pixels with the given colors",
                                params=[{"type": "list color", "length": "N", "name": "Colors"},
                                        {"type": "bool", "default": "false", "name": "Move?"},
                                        {"type": "number", "default": "1", "name": "Direction (positive = forward)"},
                                        {"type": "number", "default": "1", "name": "Duration"}])
class AlternatingColorsEffect(Effect):
    @staticmethod
    # direction 1 means forwards, direction -1 means backwards
    async def run(pixels, colors, move=False, direction=1, duration=1, *args, **kwargs):
        num_colors = len(colors)
        if not move:
            for i, pixel in enumerate(pixels):
                color = colors[i % num_colors]
                pixels[i] = gamma_correct(color)
            pixels.show()
            return
        offset = 0
        while True:
            for i, pixel in enumerate(pixels):
                color = colors[(i + offset) % num_colors]
                pixels[i] = gamma_correct(color)
            pixels.show()
            offset -= direction
            await asyncio.sleep(duration)

        

app = Flask(__name__)
CORS(app)

led_status = 0

@app.route("/api/effects/")
def effects_api():
    return engine.effects_to_json()

@app.route("/effect/run", methods=["POST"])
async def run_effect():
    json_data = request.get_json()
    await engine.run_effect(json_data["id"], **{key: val for key, val in json_data.items()})
    return jsonify({"status": "data received"})

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

@app.route("/leds/off/")
def off():
    global pixels
    pixels.fill(CLEAR)
    pixels.show()
    print("Turned off pixels")
    return "OFF"

async def main():
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

# Start the server if the script is executed directly
if __name__ == "__main__":
    # debug=True enables auto-reload on code changes
    # host="0.0.0.0" allows external access on your local network
    asyncio.run(main())
