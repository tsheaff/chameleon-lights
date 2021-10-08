import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30)
print("pixels before is", pixels)
pixels[0] = (255, 0, 0)
print("pixels  after is", pixels)
