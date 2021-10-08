import time
import board
import neopixel

FRAME_RATE = 24.0
FRAME_DURATION = (1 / FRAME_RATE)
PIN = board.D18
NUM_LEDS = 50

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

colors = [
    '#ffbe0b',
    '#fb5607',
    '#ff006e',
    '#8338ec',
    '#3a86ff',
    '#8338ec',
    '#ff006e',
    '#fb5607',
]

pixels = neopixel.NeoPixel(PIN, NUM_LEDS)

# def parity_colors(even_color, odd_color):
#     for i in range(NUM_LEDS):
#         is_even = (i % 2) == 0
#         if is_even:
#             color = even_color
#         else:
#             color = odd_color
#         pixels[i] = color

def loopPrimaryColors():
    for hex in colors:
        for i in range(NUM_LEDS):
            pixels[i] = hex_to_rgb(hex)
            time.sleep(0.75 * FRAME_DURATION)

while True:
    loopPrimaryColors()
