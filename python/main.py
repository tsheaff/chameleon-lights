import board
import neopixel
import time
import colors
import math
import random
from colour import Color

PIN = board.D18
NUM_PIXELS = 50

FRAME_RATE = 60.0
FRAME_DURATION = (1 / FRAME_RATE)

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS)
pixel_colors = map(lambda x: Color("#00ff00"), [None] * NUM_PIXELS)
print("pixel_colors", pixel_colors)
start_time = time.time()

def periodIndex(period, time_elapsed):
    return math.floor(time_elapsed / period)

def colorToRGB(color):
    return [
        math.floor(color.red * 255),
        math.floor(color.green * 255),
        math.floor(color.blue * 255),
    ]

def updateFrame(time_elapsed):
    print("update frame", time_elapsed)

def applyColors():
    for i, c in enumerate(pixel_colors):
        pixels[i] = colorToRGB(c)

while True:
    current_time = time.time()
    time_elapsed = current_time - start_time
    updateFrame(time_elapsed)
    applyColors()
    time.sleep(FRAME_DURATION)

while True:
    
    time.sleep(1.0)
