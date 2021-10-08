import time
import board
import neopixel

sleep_duration = 0.5

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

colors = [
    hex_to_rgb('#d9ed92'),
    hex_to_rgb('#b5e48c'),
    hex_to_rgb('#99d98c'),
    hex_to_rgb('#34a0a4'),
    hex_to_rgb('#1a759f'),
    hex_to_rgb('#184e77'),
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
