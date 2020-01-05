"""Config file.

|

  **Entity**
"""

#: Amount of entities to first spawn.
start_amount = 15
#: A random range (min, max) of the start size of entities.
start_size = (30, 60)
#: A random range (min, max) of the start speed of entities
start_speed = (3, 6)
#: How much energy the entities start with.
start_energy = 200000
#: How much energy is drained each turn, depending on speed and size.
energy_drain_formula = '0.3*speed*size'
#: How much energy each food sprite gives.
food_energy = 5000
#: The odds of a mating occurring when two entities collide.
mating_chance = 0.1
#: How big the mating counter has to be to mate.
mating_counter_roof = 2000
#: How big the age counter has to be to mate (how old the entity has to be).
mating_age_counter_roof = 800
#: How much energy is drained from a parent, dependent on energy.
mating_energy_formula = '0.25*energy'
#: The minimum energy drain from a parent (for when the parent's energy is too low)
mating_energy_formula_min = 1000
#: How much the average of the parent's speed genes are shifted.
speed_variation = (2, 4)
#: How much the average of the parent's size genes are shifted.
size_variation = (2, 4)
#: Random (min, max) range of how much the direction counter is incremented by.
direction_counter_increment = (1, 10)
#: How big the direction counter has to be to change direction.
direction_counter_roof = 100
#: Minimal speed for an entity. If it is lower than this, it is automatically set to this value.
min_speed = 1
#: Minimal size for an entity. If it is lower than this, it is automatically set to this value.
min_size = 1
#: Image of the entity.
entity_image = 'optimusfly.png'

# test

"""

|
|
|

**Food**
"""

#: How big a food sprite is.
food_size = 10
#: How many food sprites are spawned each turned.
food_amount = 10
#: How big the counter has to be to spawn the food.
food_spawn_counter_roof = 200
#: A random range (min, max) of how much the food_spawn_counter is incremented by.
food_spawn_counter_increment = (2, 5)
#: Image of the food sprite.
food_image = 'optimusfly.png'

"""

|
|
|

**Markers**
"""

#: How long the starve marker stays up.
starve_marker_duration = 22
#: Color of the starve marker.
starve_marker_color = (255, 0, 0)
#: How long the birth marker stays up.
birth_marker_duration = 22
#: Color of the birth marker.
birth_marker_color = (0, 255, 0)


"""

|
|
|

**Statistics**
"""

#: In seconds, how big the statistics counter has to be to save the current values of the entities' genes.
statistics_counter_roof = 100
#: Translation for evolution variables.
var_translation = {'speed': 'hastighet', 'size': 'storlek', 'energy': 'energi', 'amount': 'antal'}
#: Max y limits for the graphs.
ylims = {'hastighet': 30, 'storlek': 50, 'energi': start_energy, 'antal': 300}
#: Title of an average graph.
title_format = 'KEY, medelvärde'
#: File name of an average graph.
fname_format = 'KEY, medelvärde'


"""

|
|
|

**GUI**
"""

#: (width, height) of the GUI.
manual_dims = (1540, 863)
#: Frames per second. Idealized value. In reality, it will become smaller due to the program bottlenecking.
fps = 60
#: Pixels that the window roof is shrunk down by.
window_roof_offset = 31
#: Pixels that the window floor is elevated by.
window_floor_offset = 40
#: Pixels that the border rect roof is shrunk down by.
border_roof_offset = 18
#: Pixels that the border rect is shifted to the right by.
border_left_offset = 14
#: Ratio of (border width)/(window width).
border_width_factor = 0.99
#: Ratio of (border height)/(window height).
border_height_factor = 0.98
#: Border rect line thickness.
border_thick = 3
#: Border rect color.
border_color = (255, 255, 255, 255)  # White


"""

|
|
|

**Simulation**
"""

#: The format of the simulation directory.
dir_format = '%a %H.%M, %d %b'
#: Name of the main executable file.
exe = 'startworld.exe'
#: How many times the program is run.
runs = 2
#: In seconds, the duration of each run.
duration = 600



