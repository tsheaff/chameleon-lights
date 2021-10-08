import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 50)
def loopPrimaryColors():
    pixels.fill((0, 255, 0))
    time.sleep(2.0)
    pixels.fill((255, 0, 0))
    time.sleep(2.0)
    pixels.fill((0, 0, 255))
    time.sleep(2.0)

while True:
    loopPrimaryColors()

# pixels.show()
# pixels.write()
