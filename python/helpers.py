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
    point = Bezier.Curve([t], controlPoints)[0][1]
    return point[1] # return the y value for the point, which is in [x,y] form
