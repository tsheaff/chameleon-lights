import random
from colour import Color

gradient_set = [
    [
        '#ff0000', # true_red
        '#ffff00', # gold
    ],
    [
        '#ff0000', # true_red
        '#6495ed', # corn_flower 
    ],
    [
        '#ff0000', # true_red
        '#ff00ff', # true_purple
    ],
    [
        '#f04a00', # golden_gate 
        '#008000', # green
    ],
    [
        '#f04a00', # golden_gate 
        '#0000ff', # true_blue
    ],
    [
        '#f04a00', # golden_gate 
        '#8b008b', # dark_magenta
    ],
    [
        '#f04a00', # golden_gate 
        '#441166', # purple
    ],
    [
        '#ff7f50', # coral
        '#6495ed', # corn_flower 
    ],
    [
        '#ff7f50', # coral
        '#ff00ff', # true_purple
    ],
    [
        '#ffff00', # gold
        '#0000ff', # true_blue
    ],
    [
        '#ffff00', # gold
        '#008000', # green
    ],
    [
        '#7fff00', # chartreuse 
        '#441166', # purple
    ],
    [
        '#7fff00', # chartreuse 
        '#0000ff', # true_blue
    ],
    [
        '#008000', # green
        '#6495ed', # corn_flower 
    ],
    [
        '#008000', # green
        '#8b008b', # dark_magenta
    ],
    [
        '#008000', # green
        '#ff00ff', # true_purple
    ],
    [
        '#0000ff', # true_blue
        '#6495ed', # corn_flower 
    ],
    [
        '#0000ff', # true_blue
        '#ff00ff', # true_purple
    ],
    [
        '#0000ff', # true_blue
        '#8b008b', # dark_magenta
    ],
    [
        '#0000ff', # true_blue
        '#441166', # purple
    ],
    [
        '#ff0000', # true_red
        '#ff0000', # true_red
    ],
    [
        '#f04a00', # golden_gate
        '#f04a00', # golden_gate
    ],
    [
        '#ff7f50', # coral
        '#ff7f50', # coral
    ],
    [
        '#ffff00', # yellow
        '#ffff00', # yellow
    ],
    [
        '#008000', # green
        '#008000', # green
    ],
    [
        '#6495ed', # corn_flower
        '#6495ed', # corn_flower
    ],
    [
        '#ff00ff', # true_purple
        '#ff00ff', # true_purple
    ],
    [
        '#441166', # purple
        '#441166', # purple
    ],
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

def pick_next_nonflat_gradient():
    attempt = pick_next_gradient()
    if gradient_is_flat(attempt):
        # try again
        return pick_next_nonflat_gradient()
    else:
        return attempt

def gradient_is_flat(gradient):
    first_color = gradient[0]
    last_color = gradient[-1]
    return first_color == last_color


reshuffle_set()