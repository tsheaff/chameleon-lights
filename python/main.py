import time
import board
import neopixel

sleep_duration = 0.5

colors = [
    '#d9ed92',
    '#b5e48c',
    '#99d98c',
    '#34a0a4',
    '#1a759f',
    '#184e77',
    # [255, 0, 0],
    # [255, 255, 0],
    # [0, 255, 0],
    # [0, 255, 255],
    # [0, 0, 255],
    # [255, 0, 255],
]

pixels = neopixel.NeoPixel(board.D18, 50)
def loopPrimaryColors():
    pixels.fill(colors[0])
    time.sleep(sleep_duration)
    pixels.fill(colors[1])
    time.sleep(sleep_duration)
    pixels.fill(colors[2])
    time.sleep(sleep_duration)
    pixels.fill(colors[3])
    time.sleep(sleep_duration)
    pixels.fill(colors[4])
    time.sleep(sleep_duration)
    pixels.fill(colors[5])
    time.sleep(sleep_duration)

while True:
    loopPrimaryColors()
