from colour import Color

gradient_sets = {
    "rgb": [
        # [
        #     '#ffffff',
        #     '#000000',
        # ],
        [
            '#00ff00',
            '#ff0000',
        ],
        [
            '#ff0000',
            '#ffff00',
        ],
        [
            '#ff0000',
            '#0000ff',
        ],
        [
            '#0000ff',
            '#ffff00',
        ],
        # [
        #     '#ffffff',
        #     '#0000ff',
        # ],
        # [
        #     '#ffffff',
        #     '#ff0000',
        # ],
        # [
        #     '#ffffff',
        #     '#ff8000',
        # ],
        # [
        #     '#ffffff',
        #     '#ff00ff',
        # ],
        [
            '#00ff00',
            '#0000ff',
        ],
        [
            '#ffc8c8',
            '#ff00ff',
        ],
    ],
    # "pastel": [
    #     [
    #         '#ffbe0b',
    #         '#fb5607',
    #     ],
    #     [
    #         '#ff006e',
    #         '#8338ec',
    #     ],
    #     [
    #         '#3a86ff',
    #         '#8338ec',
    #     ],
    #     [
    #         '#ff006e',
    #         '#fb5607',
    #     ],
    # ]
}

set_name_index = 0
set_index = 0
all_set_names = list(gradient_sets.keys())

# must make sure indexes are in range first
def get_current_gradient():
    set_name = all_set_names[set_name_index]
    return gradient_sets[set_name][set_index]

def get_next_gradient():
    global set_index, set_name_index
    set_name = all_set_names[set_name_index]
    set = gradient_sets[set_name]
    if set_index >= len(set):
        set_index = 0
        set_name_index += 1
        if set_name_index >= len(all_set_names):
            set_name_index = 0
        return get_current_gradient()

    gradient = get_current_gradient()
    set_index += 1
    return gradient
    

# TODO: Shuffle, not just linear
def pick_next_gradient():
    gradient = get_next_gradient()
    print("chose gradient", gradient)
    return list(map(lambda rgb: Color(rgb), gradient))
