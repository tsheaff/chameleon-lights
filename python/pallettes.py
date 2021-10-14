from colour import Color

gradient_sets = {
    "rgb": [
        [
            '#ff0000',
            '#ffff00',
        ],
        [
            '#ff0000',
            '#ff00ff',
        ],
    ],
    "pastel": [
        [
            '#ffbe0b',
            '#fb5607',
        ],
        [
            '#ff006e',
            '#8338ec',
        ],
        [
            '#3a86ff',
            '#8338ec',
        ],
        [
            '#ff006e',
            '#fb5607',
        ],
    ]
}

set_name_index = 0
set_index = 0
all_set_names = list(gradient_sets.keys())

# TODO: Shuffle, not just linear
def pick_next_gradient():
    global set_index, set_name_index
    set_name = all_set_names[set_name_index]
    set_index += 1
    set = gradient_sets[set_name]
    if set_index >= len(set):
        set_index = 0
        set_name_index += 1
        if set_name_index >= len(all_set_names):
            set_name_index = 0
        
    color_rgb = gradient_sets[set_name][set_index]
    print("chose color", color_rgb)
    return Color(color_rgb)