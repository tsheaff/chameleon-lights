import board
import neopixel

PIN = board.D18
NUM_LEDS = 50

pixels = neopixel.NeoPixel(PIN, NUM_LEDS)
pixels.fill([0,0,0])