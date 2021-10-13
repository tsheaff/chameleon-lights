import math
from colour import Color
import bezier
import numpy as np
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
    curve = bezier.Curve(controlPoints, degree=3)

    points = curve.evaluate(t)
    print("    evaluate_bezier_at: t", t)
    print("    evaluate_bezier_at: controlPoints", controlPoints)
    print("    evaluate_bezier_at: curve", curve)
    print("    evaluate_bezier_at: points", points)
    return points[1][0]

def pixel_at(x, num_pixels):
    if x <= 0: return 0
    if x >= 1: return num_pixels - 1
    return math.floor(x * num_pixels)
