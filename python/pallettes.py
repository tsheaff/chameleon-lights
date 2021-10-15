import random
from colour import Color

gradient_set = [
    # [
    #     '#00ff00',
    #     '#ff0000',
    # ],
    # [
    #     '#ff0000',
    #     '#ffff00',
    # ],
    # [
    #     '#ff0000',
    #     '#0000ff',
    # ],
    # [
    #     '#0000ff',
    #     '#ffff00',
    # ],
    # [
    #     '#00ff00',
    #     '#0000ff',
    # ],
    # [
    #     '#ffc8c8',
    #     '#ff00ff',
    # ],
    # [
    #     '#ffffff',
    #     '#ffffff',
    # ],
    [
        '#ffff00',
        '#ffff00',
    ],
    # [
    #     '#0000ff',
    #     '#0000ff',
    # ],
    # [
    #     '#ff0000',
    #     '#ff0000',
    # ],
]

shuffle = gradient_set.copy()

set_index = 0

def reshuffle_set():
    random.shuffle(shuffle)
    print("pallette shuffle is", shuffle)

# TODO: Randomize the set first
def get_next_gradient():
    global set_index
    if set_index >= len(shuffle):
        reshuffle_set()
        set_index = 0

    gradient = shuffle[set_index]
    set_index += 1
    return gradient
    

# TODO: Shuffle, not just linear
def pick_next_gradient():
    gradient = get_next_gradient()
    print("chose gradient", gradient)
    return list(map(lambda rgb: Color(rgb), gradient))

reshuffle_set()