from logic import *
from init import *

def reset_level(current_level):
    push_group = []
    time_freeze = True
    last_keys = pygame.key.get_pressed()
    level_start_time = pygame.time.get_ticks()
    event_finished = False
    if current_level[5] > 0:
        movement = True
    else:
        movement = False
    if current_level[5] > 9:
        allow_freeze = True
    else:
        allow_freeze = False
    starting_pos = (current_level[2].body.position[0], current_level[2].body.position[1])
    return push_group, time_freeze, last_keys, level_start_time, event_finished, movement, allow_freeze, starting_pos

def light_group_setup(light_group):
    for index, light in enumerate(light_group):
        light_circle_scaled = pygame.transform.scale(light_circle, (light[1]*3, light[1]*3))
        light_circle_scaled.set_alpha(100+((light[1]/255)*100))
        light_group[index] = [*light, light_circle_scaled]
    return light_group

def setup_next_level(playerpos, currentlevel):
    next_level = f"setup_level{currentlevel[5]+2}({playerpos})"
    return eval(next_level)

def setup_level1(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                        physbox(0, -90, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                        physbox(0, 568, space, image=pygame.transform.scale(basebox_img, (1024, 300)), static=True),
                        physbox(1014, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                    ]

    pygame_group = [win_rect((0, 900), (1024, 50))]
    phys_group = []
    player_character = player_block(462, 518, space, static=False)
    light_group = light_group_setup([((100,100), 20), ((512,-200), 750)])
    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 0]

    return level_group, space

def setup_level2(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physbox(100, 668, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True)
                    ]

    pygame_group = [win_rect((0, 800), (1024, 50))]
    phys_group = []
    player_character = player_block(playerpos[0], -200, space, static = False)
    light_group = light_group_setup([((100,100), 20), ((512,-200), 750)])
    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 1]

    return level_group, space

def setup_level3(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physbox(0, 668, space, image=pygame.transform.scale(basebox_img, (824, 100)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physbox(747, 150, space, image=pygame.transform.scale(basebox_img, (127, 800)), static=True),
                    physramp((100, 418), math.radians(-45), space, image=pygame.transform.scale(basebox_img, (800, 100)), static=True)
                    ]

    pygame_group = [win_rect((0, 818), (1024, 50))]
    phys_group = []
    player_character = player_block(playerpos[0], -200, space, static = False)
    light_group = light_group_setup([((100,100), 20), ((512,-200), 750)])

    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 2]

    return level_group, space

def setup_level4(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physbox(80, 668, space, image=pygame.transform.scale(basebox_img, (144, 100)), static=True),
                    physbox(650, 668, space, image=pygame.transform.scale(basebox_img, (374, 100)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True)
                    ]

    pygame_group = [win_rect((0, 818),(100, 50)), kill_rect((100, 738), (1024, 30))]
    phys_group = []
    player_character = player_block(playerpos[0], -200, space, static = False)
    light_group = light_group_setup([((100,100), 20), ((512,-200), 750)])

    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 3]

    return level_group, space

def setup_level5(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, 668, space, image=pygame.transform.scale(basebox_img, (100, 100)), static=True),
                    physbox(800, 668, space, image=pygame.transform.scale(basebox_img, (100, 100)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physbox(800, 0, space, image=pygame.transform.scale(basebox_img, (100, 400)), static=True),
                    physbox(200, 618, space, image=pygame.transform.scale(basebox_img, (100, 20)), static=True),
                    physbox(400, 568, space, image=pygame.transform.scale(basebox_img, (100, 20)), static=True)
                    ]

    pygame_group = [win_rect((924, 818), (100, 50)), kill_rect((100, 738), (800, 30))]
    phys_group = []
    player_character = player_block(playerpos[0], -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, -200), 750)])

    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 4]

    return level_group, space
def setup_level6(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1268)), static=True),
                    physramp((150, 484), math.radians(-10),space, image=pygame.transform.scale(basebox_img, (1024, 500)), static=True)
                    ]

    pygame_group = [win_rect((0, 818), (800, 50))]
    phys_group = []
    player_character = player_block(playerpos[0], -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, -200), 750)])

    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 5]

    return level_group, space

def setup_level7(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 764)), static=True),
                    physbox(0, 384, space, image=pygame.transform.scale(basebox_img, (100, 384)), static=True),
                    physbox(0, 768, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(924, 384, space, image=pygame.transform.scale(basebox_img, (500, 384)), static=True),
                    ]

    pygame_group = [kill_rect((0, 718), (1024, 100)), win_rect((1124, 166), (500, 250))]
    phys_group = [physbox(100, 700, space, image=pygame.transform.scale(basebox_img, (800, 10)))]
    player_character = player_block(playerpos[0], -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 6]

    return level1_group, space

def setup_level8(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1164)), static=True),
                    physbox(0, 384, space, image=pygame.transform.scale(basebox_img, (100, 384)), static=True),
                    physbox(0, 758, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(864, 284, space, image=pygame.transform.scale(basebox_img, (50, 668)), static=True),
                    physramp((964, 134), math.radians(45), space, image=pygame.transform.scale(basebox_img, (100, 50)), static=True)
                    ]

    pygame_group = [win_rect((1074, 668), (100, 100))]
    phys_group = [physbox(914, 658, space, image=pygame.transform.scale(basebox_img, (75,100))), physbox(914, 588, space, image=pygame.transform.scale(basebox_img, (75,100)))]
    player_character = player_block(10, -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500), ((1300, 668), 300)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 7]

    return level1_group, space

def setup_level9(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(0, 568, space, image=pygame.transform.scale(basebox_img, (1024, 300)), static=True),
                    physbox(1014, 0, space, image=pygame.transform.scale(basebox_img, (100, 468)), static=True),
                    ]

    pygame_group = [win_rect((1000, 768), (1024, 100))]
    phys_group = []
    player_character = player_block(10, -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500), ((1300, 668), 300)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 8]

    return level1_group, space

def setup_level10(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(0, 568, space, image=pygame.transform.scale(basebox_img, (1024, 300)), static=True),
                    physbox(1014, 0, space, image=pygame.transform.scale(basebox_img, (100, 468)), static=True),
                    ]

    pygame_group = [win_rect((1000, 668), (1024, 100))]
    phys_group = []
    player_character = player_block(10, -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500), ((1300, 668), 300)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 9]

    return level1_group, space

def setup_level11(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1268)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 764)), static=True),
                    physbox(0, 384, space, image=pygame.transform.scale(basebox_img, (100, 384)), static=True),
                    physbox(0, 768, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(924, 384, space, image=pygame.transform.scale(basebox_img, (500, 384)), static=True),
                    ]

    pygame_group = [kill_rect((0, 718), (1024, 100)), win_rect((1124, 166), (500, 250))]
    phys_group = [physbox(100, 700, space, image=pygame.transform.scale(basebox_img, (800, 10)), static=True)]
    player_character = player_block(10, -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 10]

    return level1_group, space

def setup_level12(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (10, 1000)), static=True),
                    physbox(0, -500, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                    physbox(1014, -500, space, image=pygame.transform.scale(basebox_img, (100, 1264)), static=True),
                    physbox(0, 184, space, image=pygame.transform.scale(basebox_img, (100, 384)), static=True),
                    ]

    pygame_group = [kill_rect((0, 718), (1024, 100)), win_rect((-100, 500), (100, 800))]
    phys_group = [physbox(100, -400, space, image=pygame.transform.scale(basebox_img, (800, 10)), static=True)]
    player_character = player_block(10, -200, space, static=False)
    light_group = light_group_setup([((100, 100), 20), ((512, 100), 500)])
    level1_group = [phys_group, static_group, player_character, light_group, pygame_group, 11]

    return level1_group, space

def setup_level13(playerpos):
    space = pymunk.Space()  # Create a Space which contain the simulation
    space.gravity = 0, 1000  # Set its gravity

    static_group = [physbox(-90, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                        physbox(0, -90, space, image=pygame.transform.scale(basebox_img, (1024, 100)), static=True),
                        physbox(0, 568, space, image=pygame.transform.scale(basebox_img, (1024, 300)), static=True),
                        physbox(1014, 0, space, image=pygame.transform.scale(basebox_img, (100, 768)), static=True),
                    ]

    pygame_group = [win_rect((0, 900), (1024, 50))]
    phys_group = []
    for i in range(20):
        phys_group.append(physbox((50*i), 10, space, static=True))
    player_character = player_block(462, 518, space, static=False)
    light_group = light_group_setup([((100,100), 20), ((512,-200), 750)])
    level_group = [phys_group, static_group, player_character, light_group, pygame_group, 12]

    return level_group, space