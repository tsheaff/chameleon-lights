import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30)
def loopPrimaryColors():
    pixels.fill((0, 255, 0))
    time.sleep(1)
    pixels.fill((255, 0, 0))
    time.sleep(1)
    pixels.fill((255, 0, 0))

loopPrimaryColors()

# pixels.show()
# pixels.write()
