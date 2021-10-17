import board
import neopixel
import time
import helpers
from random import randrange, uniform
from colour import Color

PIN = board.D18
PIXELS_PER_STRAND = 50
NUM_STRANDS = 3
NUM_PIXELS = PIXELS_PER_STRAND * NUM_STRANDS

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False)
pixel_colors = list(map(lambda x: Color("#000000"), [None] * NUM_PIXELS))

for i in range(NUM_PIXELS):
    if (i % 3) is 0:
        pixels[i] = helpers.color_to_rgb(Color('green'))
    else:
        pixels[i] = helpers.color_to_rgb(Color('blue'))

pixels.show()

# while True:
#     print("in the loop")
#     color = helpers.random_color()
#     print("color is", color)
#     print("rgb color is", helpers.color_to_rgb(color))
#     pixels.fill(helpers.color_to_rgb(color))
#     time.sleep(2.0)
