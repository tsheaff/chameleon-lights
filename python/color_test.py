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

# def render_every_other(n):
#     for i in range(NUM_PIXELS):
#         if (i % n) is 0:
#             pixels[i] = helpers.color_to_rgb(Color('orange'))
#         else:
#             pixels[i] = helpers.color_to_rgb(Color('purple'))
#     pixels.show()

# render_every_other(2)
# time.sleep(2.0)
# render_every_other(3)
# time.sleep(2.0)
# render_every_other(4)
# time.sleep(2.0)
# render_every_other(5)
# time.sleep(2.0)
# render_every_other(4)
# time.sleep(2.0)
# render_every_other(3)
# time.sleep(2.0)
# render_every_other(2)

while True:
    print("in the loop")
    color = helpers.random_color()
    print("color is", color)
    print("rgb color is", helpers.color_to_rgb(color))
    pixels.fill(helpers.color_to_rgb(color))
    time.sleep(2.0)
