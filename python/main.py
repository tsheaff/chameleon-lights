import time
import board
import neopixel

sleep_duration = 0.2

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

colors = [
    '#10451d',
    '#155d27',
    '#1a7431',
    '#208b3a',
    '#25a244',
    '#2dc653',
    '#4ad66d',
    '#6ede8a',
    '#92e6a7',
    '#b7efc5',
    '#92e6a7',
    '#6ede8a',
    '#4ad66d',
    '#2dc653',
    '#25a244',
    '#208b3a',
    '#1a7431',
    '#155d27',
    '#10451d',
]

pixels = neopixel.NeoPixel(board.D18, 50)
def loopPrimaryColors():
    for hex in colors:
        pixels.fill(hex_to_rgb(hex))
        time.sleep(sleep_duration)

while True:
    loopPrimaryColors()
