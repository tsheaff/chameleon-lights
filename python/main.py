import time
import board
import neopixel

sleep_duration = 0.5

colors = [
    [255, 0, 0],
    [255, 255, 0],
    [0, 255, 0],
    [0, 255, 255],
    [0, 0, 255],
    [255, 0, 255],
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

# pixels.show()
# pixels.write()
