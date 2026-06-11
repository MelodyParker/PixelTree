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

def lerp(start, end, proportion):
    return start + (end - start) * proportion

try:
    while True:
        pixels.fill(CLEAR)
        print("PINK")
        for i in range(3, NUM_PIXELS):
            for j in range(10):
                pixels[i] = hsv_to_grb(7 * i, 1, j / 10)
                pixels[i-1] = hsv_to_grb(7 * (i - 1), 1, 0.9)
                pixels[i-2] = hsv_to_grb(7 * (i - 2), 1, 0.9)
                pixels[i-3] = hsv_to_grb(7 * (i - 3), 1, 0.9 - j / 10)
                pixels.show()
                time.sleep(0.005)
            #pixels[i] = hsv_to_grb(7 * i, 1, 1)
            #pixels[i+1] = hsv_to_grb(7 * (i+1), 1, 1)
            #pixels[i+2] = hsv_to_grb(7 * (i+2), 1, 1)
            #pixels.show()
            #pixels[i:i+3] = CLEAR
            #time.sleep(0.05)
        #    time.sleep(0.1)
        # 1. Fill the entire strip Blue
        #print("BLUE")
        #for i in range(NUM_PIXELS):
        #    pixels[i] = BLUE
        #    pixels.show()
        #    time.sleep(0.1)
        #pixels.show()
#        time.sleep(1)

        # 2. Change individual pixels sequentially
        # print("RED")
 #       pixels.fill(CLEAR)
  #      for i in range(NUM_PIXELS):
   #         pixels[i] = RED
    #        pixels.show()
  #          time.sleep(0.05)
 #       time.sleep(1)
#
        # 3. Fill the entire strip Green
        # print("GREEN")
     #   pixels.fill(GREEN)
      #  pixels.show()
       # time.sleep(1)

except KeyboardInterrupt:
    # Clean up and turn off LEDs on exit
    pixels.fill(CLEAR)
    pixels.show()
