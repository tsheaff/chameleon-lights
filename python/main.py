import board
import neopixel

pixels = neopixel.NeoPixel(board.D10, 30)
print("pixels before is", pixels)
pixels.fill((0, 255, 0))
print("pixels  after is", pixels)
pixels.show()
