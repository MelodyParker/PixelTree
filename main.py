from gpiozero import LED
from time import sleep

# Define the pin using its BCM GPIO number
led = LED(17)

# Loop to blink the LED forever
while True:
    led.on()       # Turns the LED on
    sleep(1)       # Wait for 1 second
    led.off()      # Turns the LED off
    sleep(1)       # Wait for 1 second
