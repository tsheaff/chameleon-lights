import board
import neopixel
import time
import math
import random
from colour import Color

PIN = board.D18
NUM_PIXELS = 50

FRAME_RATE = 20.0 # TODO: What can the human eye perceive in these LEDs? Probably not 60fps
FRAME_DURATION = (1 / FRAME_RATE)

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False)
pixel_colors = list(map(lambda x: Color("#000000"), [None] * NUM_PIXELS))
start_time = time.time()

# elapsed must be between 0 and 1
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
        self.color1 = color1
        self.color2 = color2

    def start(self):
        self.timeBegan = time.time()

    def apply(self):
        time_elapsed = time.time() - self.timeBegan
        print("GradientPulser apply: time_elapsed", time_elapsed)
        x = math.pi * time_elapsed / self.period
        print("GradientPulser apply: x", x)
        current_amplitude = math.sin(x)
        print("GradientPulser apply: current_amplitude", current_amplitude)
        color1Now = interpolateColors(self.color1, self.color2, current_amplitude)
        print("GradientPulser apply: color1Now", color1Now)
        color2Now = interpolateColors(self.color2, self.color1, current_amplitude)
        print("GradientPulser apply: color2Now", color2Now)
        applyGradient(color1Now, color2Now)

pulser = GradientPulser(3.0, Color('#ff0000'), Color('#00ffff'))
pulser.start()

while True:
    current_time = time.time()
    duration_elapsed = current_time - start_time

    updateFrame(duration_elapsed)
    applyColors()

    frame_cpu_duration = time.time() - current_time
    print("frame_cpu_duration ms:", frame_cpu_duration * 1000)
    sleep_duration = max(0, FRAME_DURATION - frame_cpu_duration)
    time.sleep(sleep_duration)
