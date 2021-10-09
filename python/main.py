import board
import neopixel
import time
import colors
import math
import random

PIN = board.D18
NUM_LEDS = 50

FRAME_RATE = 60.0
FRAME_DURATION = (1 / FRAME_RATE)

pixels = neopixel.NeoPixel(PIN, NUM_LEDS)

start_time = time.time()

def periodIndex(period, time_elapsed):
    return math.floor(time_elapsed / period)

red = 0
green = 0
blue = 0

def drawFrame(time_elapsed):
    global red, green, blue
    colorIndex = periodIndex(0.1, time_elapsed)
    distance = 3
    red += random.randint(-distance, distance)
    green += random.randint(-distance, distance)
    blue += random.randint(-distance, distance)
    print("color is", [red % 256, green % 256, blue % 256])
    pixels.fill([red % 256, green % 256, blue % 256])
    # for hex in colors.pallette:
    #     for i in range(NUM_LEDS):
    #         pixels[i] = colors.hex_to_rgb(hex)

while True:
    current_time = time.time()
    time_elapsed = current_time - start_time
    drawFrame(time_elapsed)
    time.sleep(FRAME_DURATION)
