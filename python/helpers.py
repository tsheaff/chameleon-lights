import math
from colour import Color
from Bezier import Bezier
import numpy
from random import uniform

# elapsed must be between 0 and 1
def interpolate(num1, num2, elapsed):
    return num1 + (num2 - num1) * elapsed

def interpolate_colors(color1, color2, elapsed):
    return Color(
        red=interpolate(color1.red, color2.red, elapsed),
        green=interpolate(color1.green, color2.green, elapsed),
        blue=interpolate(color1.blue, color2.blue, elapsed),
    )

def color_to_rgb(color):
    return [
        math.floor(color.red * 255),
        math.floor(color.green * 255),
        math.floor(color.blue * 255),
    ]

def random_color():
    return Color(
        red=uniform(0, 1),
        green=uniform(0, 1),
        blue=uniform(0, 1),
    )

def evaluate_bezier_at(t, controlPoints):
    points = Bezier.Curve([t], controlPoints)
    print("    evaluate_bezier_at: t", t)
    print("    evaluate_bezier_at: controlPoints", controlPoints)
    print("    evaluate_bezier_at: points", points)
    return points[0][1] # return the y value for the point, which is in [x,y] form

def pixel_at(x, num_pixels):
    if x <= 0: return 0
    if x >= 1: return num_pixels - 1
    return math.floor(x * num_pixels)
