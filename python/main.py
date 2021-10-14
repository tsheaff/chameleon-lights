import board
import neopixel
import time
import math
import helpers
from random import randrange, uniform
from easing_functions import *
from colour import Color
from enum import Enum
import numpy as np

class AnimatorType(Enum):
    CASCADE = 1
    TWINKLE = 2
    # TODO: Add More

# abstract superclass for Cascaded and all Steady States
class Animator:
    def __init__(self, duration, type):
        self.duration = duration
        self.type = type
        self.previous_colors = conductor.pixel_colors.copy()

    def update_frame():
        print("should override `update_frame` on Animator subclass")

    def start(self):
        self.time_began = time.time()

    def stop(self):
        self.time_began = None

    @property
    def is_stopped(self):
        return self.time_began == None

class Cascade(Animator):
    def __init__(self, duration, gradient, easing_curve, starting_position):
        print("   Cascade: duration", duration)
        print("   Cascade: gradient", gradient)
        print("   Cascade: easing_curve", easing_curve)
        print("   Cascade: starting_position", starting_position)
        self.duration = duration
        self.gradient = gradient
        self.easing_curve = easing_curve
        self.starting_position = starting_position

        super().__init__(duration, AnimatorType.CASCADE)

    def color_at(self, progress):
        start_color = self.gradient[0]
        end_color = self.gradient[1]
        return helpers.interpolate_colors(start_color, end_color, progress)

    def update_frame(self):
        print("   Cascade update_frame")
        if self.is_stopped:
            return False

        time_elapsed = time.time() - self.time_began
        progress = time_elapsed / self.duration

        curved_progress = helpers.evaluate_bezier_at(progress, self.easing_curve)
        end = curved_progress * (1 - self.starting_position) + self.starting_position
        start = (1 - curved_progress) * self.starting_position
        print("   Cascade update_frame: curved_progress", curved_progress)

        start_index, start_remainder = helpers.pixel_at(start, Conductor.NUM_PIXELS)
        end_index, end_remainder = helpers.pixel_at(end, Conductor.NUM_PIXELS)

        print("   Cascade update_frame: start_index, start_remainder", start_index, start_remainder)
        print("   Cascade update_frame:     end_index, end_remainder", end_index, end_remainder)

        for i in range(start_index, min(end_index + 1, Conductor.NUM_PIXELS - 1)):
            pixel_progress = i / (Conductor.NUM_PIXELS - 1)

            if i == start_index:
                color_ratio = 1 - start_remainder
            elif i == end_index:
                color_ratio = end_remainder
            else:
                color_ratio = 1

            full_color = self.color_at(pixel_progress)
            actual_color = full_color if color_ratio is 1 else helpers.interpolate_colors(self.previous_colors[i], full_color, color_ratio)
            print("   Cascade update_frame: LOOP: index, color", i, actual_color)
            conductor.pixel_colors[i] = actual_color

        if progress >= 1:
            self.stop()
            return False

        return True

class RandomCascade(Cascade):
    MIN_DURATION = 8.0
    MAX_DURATION = 20.0

    MIN_STARTING_POSITION = 0.2
    MAX_STARTING_POSITION = 0.8

    def __init__(self):
        duration = uniform(RandomCascade.MIN_DURATION, RandomCascade.MAX_DURATION)

        # TODO: Pick from a pallette, avoiding repeats (eg shuffle then iterate)
        gradient = [
            helpers.random_color(),
            helpers.random_color(),
        ]

        easing_curve = np.asfortranarray([
            [ 0.0, uniform(0, 1), uniform(0, 1), 1.0 ],
            [ 0.0, uniform(0, 1), uniform(0, 1), 1.0 ],
        ])

        starting_position = uniform(RandomCascade.MIN_STARTING_POSITION, RandomCascade.MAX_STARTING_POSITION)

        super().__init__(duration, gradient, easing_curve, starting_position)

class Twinkle(Animator):
    MIN_DURATION = 5.0
    MAX_DURATION = 10.0

    def __init__(self):
        duration = uniform(Twinkle.MIN_DURATION, Twinkle.MAX_DURATION)
        super().__init__(duration, AnimatorType.TWINKLE)

class Conductor:
    PIN = board.D18
    PIXELS_PER_STRAND = 50
    NUM_STRANDS = 1
    NUM_PIXELS = PIXELS_PER_STRAND * NUM_STRANDS

    FRAME_RATE = 20.0
    FRAME_DURATION = (1 / FRAME_RATE)

    def __init__(self):
        self.pixels = neopixel.NeoPixel(Conductor.PIN, Conductor.NUM_PIXELS, auto_write=False)
        self.pixel_colors = list(map(lambda x: Color("#000000"), [None] * Conductor.NUM_PIXELS))
        self.current_animator = None

    def get_next_animator(self, previous_animator):
        if previous_animator is None:
            return RandomCascade()

        previous_type = self.current_animator.type

        if previous_type == AnimatorType.CASCADE:
            # TODO: Randomly pick from stady-states?
            return Twinkle()
        else:
            # TODO: Always from non-cascade to cascade, or ever multiple steady states?
            return RandomCascade()

    def start_next_animator(self):
        if self.current_animator is not None:
            self.current_animator.stop()

        self.current_animator = self.get_next_animator(self.current_animator)
        self.current_animator.start()

    def update_frame(self, duration_elapsed):
        if self.current_animator is None or self.current_animator.is_stopped:
            self.start_next_animator()

        is_alive = self.current_animator.update_frame()
        if not is_alive:
            self.start_next_animator()

    def apply_colors(self):
        for i, c in enumerate(self.pixel_colors):
            self.pixels[i] = helpers.color_to_rgb(c)
        self.pixels.show()

    def start(self):
        self.start_time = time.time()

        while True:
            current_time = time.time()
            duration_elapsed = current_time - self.start_time

            self.update_frame(duration_elapsed)
            self.apply_colors()

            frame_cpu_duration = time.time() - current_time
            print("FRAME: frame_cpu_duration ms:", frame_cpu_duration * 1000)
            sleep_duration = max(0, Conductor.FRAME_DURATION - frame_cpu_duration)
            time.sleep(sleep_duration)

conductor = Conductor()
conductor.start()