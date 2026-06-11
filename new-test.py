from rpi_ws281x import PixelStrip, Adafruit_NeoPixel, Color
import time

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

try:
    while True:
        # Example: Writing one pixel at a time without breaking
        for i in range(strip.numPixels()):
            # Change the internal buffer first
            strip.setPixelColor(i, Color(255, 0, 0)) # Red
            
            # ONLY call show() once per meaningful update
            strip.show() 
            time.sleep(0.05)
            
            strip.setPixelColor(i, Color(0, 0, 0)) # Turn it back off
            
except KeyboardInterrupt:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

