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

    def update_frame(self):
        print("should override `update_frame` on Animator subclass")
        return False

    def start(self):
        print("Inside Animator start", self)
        self.time_began = time.time()

    def stop(self):
        print("Inside Animator stop", self)
        self.time_began = None

    @property
    def is_stopped(self):
        return self.time_began == None

    @property
    def num_pixels(self):
        return Conductor.NUM_PIXELS

    @property
    def time_elapsed(self):
        return time.time() - self.time_began

    @property
    def progress(self):
        return self.time_elapsed / self.duration

class Cascade(Animator):
    def __init__(self, duration, gradient, easing_curve, starting_position):
        self.duration = duration
        self.gradient = gradient
        self.easing_curve = easing_curve
        self.starting_position = starting_position
        super().__init__(duration, AnimatorType.CASCADE)

        print("Starting new CASCADE")
        print("   --> duration", self.duration)
        print("   --> gradient", self.gradient)
        print("   --> easing_curve", self.easing_curve)
        print("   --> starting_position", self.starting_position)

    def color_at(self, progress):
        start_color = self.gradient[0]
        end_color = self.gradient[1]
        return helpers.interpolate_colors(start_color, end_color, progress)

    def update_frame(self):
        if self.is_stopped:
            return False

        curved_progress = helpers.evaluate_bezier_at(self.progress, self.easing_curve)
        end = curved_progress * (1 - self.starting_position) + self.starting_position
        start = (1 - curved_progress) * self.starting_position

        start_index, start_remainder = helpers.pixel_at(start, self.num_pixels)
        end_index, end_remainder = helpers.pixel_at(end, self.num_pixels)

        for i in range(start_index, min(end_index + 1, self.num_pixels - 1)):
            pixel_progress = i / (self.num_pixels - 1)

            if i == start_index:
                color_ratio = 1 - start_remainder
            elif i == end_index:
                color_ratio = end_remainder
            else:
                color_ratio = 1

            full_color = self.color_at(pixel_progress)
            actual_color = full_color if color_ratio is 1 else helpers.interpolate_colors(self.previous_colors[i], full_color, color_ratio)
            conductor.pixel_colors[i] = actual_color

        if self.progress >= 1:
            return False

        return True

class RandomCascade(Cascade):
    MIN_DURATION = 3.0
    MAX_DURATION = 5.0

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
        self.pixel_periods = map(lambda n: uniform(0.1, 1.0), [0] * self.num_pixels)

        print("Starting new Twinkle")
        print("   --> duration", self.duration)
        print("   --> pixel_periods", self.pixel_periods)

    def update_frame(self):
        print("Twinkle update frame", self.time_began, self.is_stopped)
        if self.is_stopped:
            print("  ---> Twinkle is stopped")
            return False

        black = Color('#000000')
        for i, period in enumerate(self.pixel_periods):
            intensity = 0.5 * math.cos(math.pi * self.time_elapsed / period) + 0.5
            print("Twinkle: (i, intensity)", i, intensity)
            original_color = self.previous_colors[i]
            conductor.pixel_colors[i] = helpers.interpolate_colors(black, original_color, intensity)

        if self.progress >= 1:
            return False

        return True

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
        print("Inside get_next_animator")
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
        print("Inside start_next_animator")
        if self.current_animator is not None:
            self.current_animator.stop()

        self.current_animator = self.get_next_animator(self.current_animator)
        self.current_animator.start()

    def update_frame(self):
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
            frame_start_time = time.time()

            self.update_frame()
            self.apply_colors()

            frame_cpu_duration = time.time() - frame_start_time
            sleep_duration = max(0, Conductor.FRAME_DURATION - frame_cpu_duration)
            print("FRAME: CPU and Sleep Durations (ms):", frame_cpu_duration * 1000, sleep_duration * 1000)
            time.sleep(sleep_duration)

conductor = Conductor()
conductor.start()