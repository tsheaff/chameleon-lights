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

def updateFrame(duration_elapsed):
    pulser.apply()

def applyColors():
    for i, c in enumerate(pixel_colors):
        pixels[i] = colorToRGB(c)
    pixels.show()

def applyGradient(color1, color2):
    for i, c in enumerate(pixel_colors):
        pixel_colors[i] = interpolateColors(color1, color2, i / NUM_PIXELS)

class GradientPulser:
    def __init__(self, period, color1, color2):
        self.period = period
        self._color1 = color1
        self._color2 = color2

    def start(self):
        self.timeBegan = time.time()

    def apply(self):
        time_elapsed = time.time() - self.timeBegan
        x = time_elapsed / self.period
        current_amplitude = math.sin(x)
        color1Now = interpolateColors(self.color1, self.color2, current_amplitude)
        color2Now = interpolateColors(self.color2, self.color1, current_amplitude)
        applyGradient(color1Now, color2Now)

pulser = GradientPulser(3.0, Color('red'), Color('blue'))
pulser.start()

while True:
    current_time = time.time()
    duration_elapsed = current_time - start_time

    updateFrame(duration_elapsed)
    applyColors()

    color1 = Color("#ff0000")
    color2 = Color("#00ffff")

    frame_cpu_duration = time.time() - current_time
    sleep_duration = max(0, FRAME_DURATION - frame_cpu_duration)
    time.sleep(sleep_duration)
