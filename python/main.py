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
    print("updateFrame", duration_elapsed)
    # pulser.apply()
    for streaker in streakers:
        streaker.apply()

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
        x = math.pi * time_elapsed / self.period
        current_amplitude = abs(math.sin(x))
        color1Now = interpolateColors(self.color1, self.color2, current_amplitude)
        color2Now = interpolateColors(self.color2, self.color1, current_amplitude)
        applyGradient(color1Now, color2Now)

class Streaker:
    # speed in pixels per second
    def __init__(self, speed, color):
        self.speed = speed
        self.color = color
        self.isStopped = False

    def start(self):
        self.timeBegan = time.time()

    def stop(self):
        self.isStopped = True

    def apply(self):
        # TODO: Actually dealloc it
        if self.isStopped:
            return

        time_elapsed = time.time() - self.timeBegan
        max_pixel = min(NUM_PIXELS, math.floor(self.speed * time_elapsed))
        for i in range(0, max_pixel):
            pixel_colors[i] = self.color

        if max_pixel == NUM_PIXELS:
            self.stop()

# pulser = GradientPulser(9.0, Color('red'), Color('blue'))
# pulser.start()

def frameIndexAt(duration_elapsed):
    return math.floor(duration_elapsed / FRAME_DURATION)

streakers = []

def makeStreakerConfig(time, color, speed):
    return {
        "frame": frameIndexAt(time),
        "color": color,
        "speed": speed,
    }

streakerConfig = [
    makeStreakerConfig(0.0, 'red', 35),
    makeStreakerConfig(4.0, 'green', 80),
    makeStreakerConfig(9.0, 'blue', 20),
]

frame_index = 0

while True:
    current_time = time.time()
    duration_elapsed = current_time - start_time

    for config in streakerConfig:
        if frame_index == config["frame"]:
            streaker = Streaker(config["speed"], Color(config["color"]))
            streakers.append(streaker)
            streaker.start()

    updateFrame(duration_elapsed)
    applyColors()

    frame_cpu_duration = time.time() - current_time
    print("frame_cpu_duration ms:", frame_cpu_duration * 1000)
    sleep_duration = max(0, FRAME_DURATION - frame_cpu_duration)
    time.sleep(sleep_duration)

    frame_index += 1
