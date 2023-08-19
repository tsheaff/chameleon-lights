import random
from colour import Color

# all the colors in the pallette
# '#dc143c', # crimson
# '#f04a00', # golden_gate 
# '#ff7f50', # coral
# '#ffd700', # gold
# '#ffff00', # yellow
# '#ccdd55', # light_green
# '#7fff00', # chartreuse 
# '#008000', # green
# '#66ffff', # baby_blue
# '#6495ed', # corn_flower 
# '#4169e1', # royal_blue
# '#775588', # joanie_purple
# '#8b008b', # dark_magenta
# '#441166', # purple
# '#ffffff', # white

gradient_set = [
    [
        '#dc143c', # crimson
        '#ffd700', # gold
    ],
    [
        '#dc143c', # crimson
        '#ffffff', # white
    ],
    [
        '#dc143c', # crimson
        '#775588', # joanie_purple
    ],
    [
        '#f04a00', # golden_gate 
        '#008000', # green
    ],
    [
        '#f04a00', # golden_gate 
        '#4169e1', # royal_blue
    ],
    [
        '#f04a00', # golden_gate 
        '#8b008b', # dark_magenta
    ],
    [
        '#ff7f50', # coral
        '#6495ed', # corn_flower 
    ],
    [
        '#ff7f50', # coral
        '#775588', # joanie_purple
    ],
    [
        '#ffd700', # gold
        '#66ffff', # baby_blue
    ],
    [
        '#ffd700', # gold
        '#008000', # green
    ],
    [
        '#7fff00', # chartreuse 
        '#4169e1', # royal_blue
    ],
    [
        '#7fff00', # chartreuse 
        '#441166', # purple
    ],
    [
        '#7fff00', # chartreuse 
        '#ffffff', # white
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
        '#ffffff', # white
    ],
    [
        '#66ffff', # baby_blue
        '#6495ed', # corn_flower 
    ],
    [
        '#66ffff', # baby_blue
        '#775588', # joanie_purple
    ],
    [
        '#66ffff', # baby_blue
        '#ffffff', # white
    ],
    [
        '#4169e1', # royal_blue
        '#8b008b', # dark_magenta
    ],
    [
        '#4169e1', # royal_blue
        '#441166', # purple
    ],
    [
        '#dc143c', # crimson
        '#dc143c', # crimson
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
        '#775588', # joanie_purple
        '#775588', # joanie_purple
    ],
    [
        '#441166', # purple
        '#441166', # purple
    ],
    [
        '#ffffff', # white
        '#ffffff', # white
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