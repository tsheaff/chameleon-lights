import board
import neopixel
import time
import math
import random
from colour import Color

PIN = board.D18
NUM_PIXELS = 50

FRAME_RATE = 60.0
FRAME_DURATION = (1 / FRAME_RATE)

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False)
pixel_colors = list(map(lambda x: Color("#000000"), [None] * NUM_PIXELS))
print("pixel_colors", pixel_colors)
start_time = time.time()

def interpolate(num1, num2, elapsed):
    return num1 + (num2 - num1) * elapsed

def interpolateColors(color1, color2, elapsed):
    return Color(
        red=interpolate(color1.red, color2.red, elapsed),
        green=interpolate(color1.green, color2.green, elapsed),
        blue=interpolate(color1.blue, color2.blue, elapsed),
    )

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
    pixels.show()

def applyGradient():
    color1 = Color("#ff0000")
    color2 = Color("#00ffff")
    for i, c in enumerate(pixel_colors):
        pixel_colors[i] = interpolateColors(color1, color2, i / NUM_PIXELS)

applyGradient()
applyColors()
print("pixels", pixels)

while True:
    current_time = time.time()
    time_elapsed = current_time - start_time

    updateFrame(time_elapsed)
    applyColors()

    frame_clock_time = time.time() - current_time
    sleep_time = max(0, FRAME_DURATION - frame_clock_time)
    time.sleep(sleep_time)
