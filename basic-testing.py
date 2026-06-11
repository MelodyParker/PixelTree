import time
import board
import neopixel

# Configure the system variables
PIXEL_PIN = board.D18       # GPIO pin used
NUM_PIXELS = 50             # Number of NeoPixels in your strip
BRIGHTNESS = 0.5            # Set brightness level (0.0 to 1.0)

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=BRIGHTNESS, 
    auto_write=False
)

# Define custom color tuples (Red, Green, Blue)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CLEAR = (0, 0, 0)

print("Starting stuff")

try:
    while True:
        # 1. Fill the entire strip Blue
        print("BLUE")
        pixels.fill(BLUE)
        pixels.show()
        time.sleep(1)

        # 2. Change individual pixels sequentially
        print("RED")
        pixels.fill(CLEAR)
        for i in range(NUM_PIXELS):
            pixels[i] = RED
            pixels.show()
            time.sleep(0.05)
        time.sleep(1)

        # 3. Fill the entire strip Green
        print("GREEN")
        pixels.fill(GREEN)
        pixels.show()
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up and turn off LEDs on exit
    pixels.fill(CLEAR)
    pixels.show()