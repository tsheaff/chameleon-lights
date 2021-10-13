import board
import neopixel
import time
import math
import helpers
from random import randrange, uniform
from easing_functions import *
from colour import Color
from enum import Enum

class AnimationMode(Enum):
    CASCADE = 1
    STEADY = 2

PIN = board.D18
NUM_PIXELS = 50

FRAME_RATE = 20.0 # TODO: What can the human eye perceive in these LEDs? Probably not 60fps
FRAME_DURATION = (1 / FRAME_RATE)

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False)
pixel_colors = list(map(lambda x: Color("#000000"), [None] * NUM_PIXELS))
start_time = time.time()

cascade = None

def update_frame(duration_elapsed):
    global cascade
    print("update_frame", duration_elapsed)

    if cascade is None or cascade.is_stopped:
        cascade = RandomCascade()

    did_finish = cascade.apply()
    if did_finish:
        cascade = RandomCascade()

def apply_colors():
    for i, c in enumerate(pixel_colors):
        pixels[i] = helpers.color_to_rgb(c)
    pixels.show()

class Cascade:
    def __init__(self, duration, gradient, easing_curve, starting_position):
        self.duration = duration
        self.gradient = gradient
        self.easing_curve = easing_curve
        self.starting_position = starting_position
        self.is_stopped = False

    def start(self):
        self.time_began = time.time()

    def stop(self):
        self.is_stopped = True

    def color_at(self, progress):
        start_color = self.gradient[0]
        end_color = self.gradient[0]
        return helpers.interpolate_colors(start_color, end_color, progress)

    def apply(self):
        if self.is_stopped:
            return False

        time_elapsed = time.time() - self.time_began
        progress = time_elapsed / self.duration

        curved_progress = helpers.evaluate_bezier_at(progress, self.easing_curve)
        end = curved_progress * (1 - self.starting_position) + self.starting_position
        start = (1 - curved_progress) * self.starting_position

        start_pixel = math.floor(NUM_PIXELS * start)
        end_pixel = math.floor(NUM_PIXELS * end)

        if start_pixel == end_pixel:
            # don't divide by zero, just do nothing
            # until at least one pixel is showing
            return True

        for i in range(start_pixel, end_pixel + 1):
            pixel_progress = (i - start_pixel) / (end_pixel - start_pixel)
            pixel_colors[i] = self.color_at(pixel_progress)

        if progress >= 1:
            self.stop()
            return False

        return True

MIN_DURATION = 3.0
MAX_DURATION = 20.0

class RandomCascade(Cascade):
    def __init__(self):
        duration = uniform(MIN_DURATION, MAX_DURATION)

        # TODO: Pick from a pallette, avoiding repeats (eg shuffle then iterate)
        gradient = [
            helpers.random_color(),
            helpers.random_color(),
        ]

        easing_curve = [
            [ uniform(0, 1), uniform(0, 3) ],
            [ uniform(0, 1), uniform(0, 3) ],
        ]
        starting_position = uniform(0, 1)
        super().__init__(duration, gradient, easing_curve, starting_position)

def frameIndexAt(duration_elapsed):
    return math.floor(duration_elapsed / FRAME_DURATION)

frame_index = 0

while True:
    current_time = time.time()
    duration_elapsed = current_time - start_time

    update_frame(duration_elapsed)
    apply_colors()

    frame_cpu_duration = time.time() - current_time
    print("frame_cpu_duration ms:", frame_cpu_duration * 1000)
    sleep_duration = max(0, FRAME_DURATION - frame_cpu_duration)
    time.sleep(sleep_duration)

    frame_index += 1
