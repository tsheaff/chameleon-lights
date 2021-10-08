import board
import neopixel
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

pixels = neopixel.NeoPixel(Pin(12), 30)
print("pixels before is", pixels)
pixels[0] = (255, 0, 0)
print("pixels  after is", pixels)
