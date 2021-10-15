import board
import neopixel
import time
import math
import helpers
import pallettes
import random
import easing_functions
from colour import Color
from enum import Enum
import numpy as np

class AnimatorType(Enum):
    CASCADE = 1
    TWINKLE = 2
    PULSE = 3
    SWEEP = 4

AnimatorTypeMax = AnimatorType.SWEEP

NormalizedEaseInOut = easing_functions.QuadEaseInOut(start=0, end=1, duration = 1)

class Animator:
    def __init__(self, type, duration, buffer_duration):
        self.type = type
        self.duration = duration
        self.buffer_duration = buffer_duration
        self.buffer_began = None
        self.previous_colors = conductor.last_cascaded_colors

    def update_frame(self):
        print("ERROR: should override `update_frame` on Animator subclass", flush=True)
        return False

    def start(self):
        print("Inside Animator start", self, flush=True)
        self.time_began = time.time()

    def stop(self):
        print("Inside Animator stop", self, flush=True)
        self.time_began = None

    def start_buffer_if_necessary(self):
        if self.buffer_began is None:
            print("starting buffer", self.buffer_duration, flush=True)
            self.buffer_began = time.time()

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

    @property
    def buffer_progress(self):
        if self.buffer_began is None: return 0
        return (time.time() - self.buffer_began) / self.buffer_duration

class Cascade(Animator):
    def __init__(self, duration, gradient, easing_curve, starting_position):
        self.gradient = gradient
        self.easing_curve = easing_curve
        self.starting_position = starting_position
        buffer_duration = 0
        super().__init__(AnimatorType.CASCADE, duration, buffer_duration)

        print("Starting new CASCADE", flush=True)
        print("    --> duration", self.duration, flush=True)
        print("    --> gradient", self.gradient, flush=True)
        print("    --> easing_curve", self.easing_curve, flush=True)
        print("    --> starting_position", self.starting_position, flush=True)

    def color_at(self, progress):
        start_color = self.gradient[0]
        end_color = self.gradient[1]
        return helpers.interpolate_colors(start_color, end_color, progress)

    def stop(self):
        super().stop()
        conductor.last_cascaded_colors = conductor.pixel_colors.copy()

    def update_frame(self):
        if self.is_stopped:
            return False

        curved_progress = helpers.evaluate_bezier_at(self.progress, self.easing_curve)
        self.update_with_progress(curved_progress)

        if self.progress >= 1:
            self.update_with_progress(1.0)
            return False

        return True

    def update_with_progress(self, curved_progress):
        end = curved_progress * (1 - self.starting_position) + self.starting_position
        start = (1 - curved_progress) * self.starting_position

        start_index, start_remainder = helpers.pixel_at(start, self.num_pixels)
        end_index, end_remainder = helpers.pixel_at(end, self.num_pixels)

        for i in range(start_index, min(end_index + 1, self.num_pixels)):
            pixel_progress = i / (self.num_pixels - 1)

            if i == start_index:
                color_ratio = 1 - start_remainder
            elif i == end_index:
                if i == (self.num_pixels - 1):
                    color_ratio = 1
                else:
                    color_ratio = end_remainder
            else:
                color_ratio = 1

            full_color = self.color_at(pixel_progress)
            actual_color = full_color if color_ratio is 1 else helpers.interpolate_colors(self.previous_colors[i], full_color, color_ratio)
            conductor.pixel_colors[i] = actual_color


class RandomCascade(Cascade):
    MIN_DURATION = 3.0
    MAX_DURATION = 30.0

    MIN_STARTING_POSITION = 0.05
    MAX_STARTING_POSITION = 0.95

    def __init__(self):
        duration = random.uniform(RandomCascade.MIN_DURATION, RandomCascade.MAX_DURATION)

        gradient = pallettes.pick_next_gradient()

        easing_curve = np.asfortranarray([
            [ 0.0, random.uniform(0, 1), random.uniform(0, 1), 1.0 ],
            [ 0.0, random.uniform(0, 1), random.uniform(0, 1), 1.0 ],
        ])

        starting_position = random.uniform(RandomCascade.MIN_STARTING_POSITION, RandomCascade.MAX_STARTING_POSITION)

        super().__init__(duration, gradient, easing_curve, starting_position)

class Twinkle(Animator):
    MIN_DURATION = 5.0
    MAX_DURATION = 30.0

    MIN_TWINKLE_PERIOD = 0.2
    MAX_TWINKLE_PERIOD = 2.0

    def __init__(self):
        duration = random.uniform(Twinkle.MIN_DURATION, Twinkle.MAX_DURATION)
        buffer_duration = 3.0
        super().__init__(AnimatorType.TWINKLE, duration, buffer_duration)
        self.twinkle_periods = list(map(lambda n: random.uniform(Twinkle.MIN_TWINKLE_PERIOD, Twinkle.MAX_TWINKLE_PERIOD), [0] * self.num_pixels))

        print("Starting new Twinkle", flush=True)
        print("    --> duration", self.duration, flush=True)
        print("    --> twinkle_periods length", len(self.twinkle_periods), flush=True)

    def update_frame(self):
        if self.is_stopped:
            return False

        progress = self.progress
        buffer_progress = self.buffer_progress
        curved_buffer_progress = 0 if buffer_progress is 0 else NormalizedEaseInOut.ease(buffer_progress)
        if progress >= 1:
            self.start_buffer_if_necessary()
            if buffer_progress >= 1:
                return False

        black = Color('#000000')
        for i, period in enumerate(self.twinkle_periods):
            intensity = 0.5 * math.cos(math.pi * self.time_elapsed / period) + 0.5
            buffered_intensity = intensity - (intensity - 1) * curved_buffer_progress
            original_color = self.previous_colors[i]
            conductor.pixel_colors[i] = helpers.interpolate_colors(black, original_color, buffered_intensity)

        return True

class Pulse(Animator):
    MIN_DURATION = 5.0
    MAX_DURATION = 20.0

    MIN_PERIOD = 0.2
    MAX_PERIOD = 3.0

    def __init__(self):
        duration = random.uniform(Pulse.MIN_DURATION, Pulse.MAX_DURATION)
        buffer_duration = 3.0
        super().__init__(AnimatorType.PULSE, duration, buffer_duration)
        self.period = random.uniform(Pulse.MIN_PERIOD, Pulse.MAX_PERIOD)

        print("Starting new Pulse", flush=True)
        print("    --> duration", self.duration, flush=True)
        print("    --> period", self.period, flush=True)

    def update_frame(self):
        if self.is_stopped:
            return False

        progress = self.progress
        buffer_progress = self.buffer_progress
        curved_buffer_progress = 0 if buffer_progress is 0 else NormalizedEaseInOut.ease(buffer_progress)
        if progress >= 1:
            self.start_buffer_if_necessary()
            if buffer_progress >= 1:
                return False

        black = Color('#000000')
        intensity = 0.5 * math.cos(math.pi * self.time_elapsed / self.period) + 0.5
        buffered_intensity = intensity - (intensity - 1) * curved_buffer_progress
        for i in range(0, self.num_pixels):
            original_color = self.previous_colors[i]
            conductor.pixel_colors[i] = helpers.interpolate_colors(black, original_color, buffered_intensity)

        return True

class Sweep(Animator):
    MIN_DURATION = 5.0
    MAX_DURATION = 20.0

    MIN_PERIOD = 0.2
    MAX_PERIOD = 3.0

    def __init__(self):
        duration = random.uniform(Sweep.MIN_DURATION, Sweep.MAX_DURATION)
        buffer_duration = 3.0
        super().__init__(AnimatorType.SWEEP, duration, buffer_duration)
        self.period = random.uniform(Sweep.MIN_PERIOD, Sweep.MAX_PERIOD)

        print("Starting new Sweep", flush=True)
        print("    --> duration", self.duration, flush=True)
        print("    --> period", self.period, flush=True)

    def update_frame(self):
        if self.is_stopped:
            return False

        progress = self.progress
        buffer_progress = self.buffer_progress
        curved_buffer_progress = 0 if buffer_progress is 0 else NormalizedEaseInOut.ease(buffer_progress)
        if progress >= 1:
            self.start_buffer_if_necessary()
            if buffer_progress >= 1:
                return False

        intensity = 0.5 * math.cos(math.pi * self.time_elapsed / self.period) + 0.5
        buffered_intensity = intensity - (intensity - 1) * curved_buffer_progress
        for i in range(0, self.num_pixels):
            inverted_i = self.num_pixels - 1 - i
            inverted_color = self.previous_colors[inverted_i]
            original_color = self.previous_colors[i]
            conductor.pixel_colors[i] = helpers.interpolate_colors(inverted_color, original_color, buffered_intensity)

        return True

class Conductor:
    PIN = board.D18
    PIXELS_PER_STRAND = 50
    NUM_STRANDS = 3
    NUM_PIXELS = PIXELS_PER_STRAND * NUM_STRANDS

    FRAME_RATE = 10.0
    FRAME_DURATION = (1 / FRAME_RATE)

    def __init__(self):
        self.pixels = neopixel.NeoPixel(Conductor.PIN, Conductor.NUM_PIXELS, auto_write=False)
        self.pixel_colors = list(map(lambda x: Color("#000000"), [None] * Conductor.NUM_PIXELS))
        self.last_cascaded_colors = self.pixel_colors.copy()
        self.current_animator = None

    def get_random_type(self):
        return random.choice(list(AnimatorType))

    def get_next_animator(self, previous_animator):
        if previous_animator is None:
            return RandomCascade()

        type = self.get_random_type()
        if type == AnimatorType.CASCADE:
            return RandomCascade()
        elif type == AnimatorType.TWINKLE:
            return Twinkle()
        elif type == AnimatorType.PULSE:
            return Pulse()
        elif type == AnimatorType.SWEEP:
            return Sweep()

    def start_next_animator(self):
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
            # print("FRAME: CPU and Sleep Durations (ms):", frame_cpu_duration * 1000, sleep_duration * 1000, flush=True)
            time.sleep(sleep_duration)

conductor = Conductor()
conductor.start()