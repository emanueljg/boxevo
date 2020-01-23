"""A module containing all variables that modify the behaviour of most modules."""

############entity############

#: Amount of entities to first spawn.
start_amount = 15
#: A random interval of the start size of entities.
start_size = (30, 40)
#: A random interval (min, max) of the start speed of entities
start_speed = (3, 6)
#: How much energy the entities start with.
start_energy = 200000
#: How much energy is drained each turn, depending on speed and size.
energy_drain_formula = '0.3*speed*size'
#: The odds of a mating occurring when two entities collide.
mating_chance = 0.1
#: How big the mating counter has to be to mate.
mating_counter_roof = 2000
#: How big the age counter has to be to mate (how old the entity has to be).
mating_age_counter_roof = 800
#: How much energy is drained from a parent, dependent on energy.
mating_energy_formula = '0.25*energy'
#: The minimum energy drain from a parent
#:  (for when the parent's energy is too low to be transferred proportionally).
mating_energy_formula_min = 1000
#: A random interval of how much the average of the parents' speed genes are shifted.
speed_variation = (2, 4)
#: A random interval of how much the average of the parents' size genes are shifted.
size_variation = (2, 4)
#: A random interval of how much the direction counter is incremented by.
direction_counter_increment = (1, 10)
#: How big the direction counter has to be to change direction.
direction_counter_roof = 100
#: Minimal speed for an entity. If the entity speed is lower than this, it is automatically set to this value.
min_speed = 1
#: Minimal size for an entity. If the entity size is lower than this, it is automatically set to this value.
min_size = 1
#: Image of the entity.
entity_image = 'entity.png'

############food############

#: How big a food sprite is.
food_size = 10
#: How many food sprites are spawned each turned.
food_amount = 10
#: How much energy each food sprite gives.
food_energy = 5000
#: How big the counter has to be to spawn the food.
food_spawn_counter_roof = 200
#: A random interval of how much the spawn_counter is incremented by.
food_spawn_counter_increment = (2, 5)
#: Image of the food.
food_image = 'food.png'

############marker############

#: How long the starve marker stays up.
starve_marker_duration = 22
#: Color of the starve marker.
starve_marker_color = (255, 0, 0)
#: How long the birth marker stays up.
birth_marker_duration = 22
#: Color of the birth marker.
birth_marker_color = (0, 255, 0)

############graph############

#: In seconds, how big the statistics counter has to be to save the current values of the entities' genes.
statistics_counter_roof = 100
#: Translation for evolution variables.
var_translation = {'speed': 'hastighet', 'size': 'storlek', 'energy': 'energi', 'amount': 'antal'}
#: Variables that should be scaled. The new var will be the old var divided by these values.
scaled_vars = {'energi': 1000}
#: Max y limits for the graphs.
ylims = {'hastighet': 10, 'storlek': 40, 'energi': 200, 'antal': 300}
#: Labels of the x and y axis.
axis_labels = {'x': 'Tid (s)', 'hastighet': 'Hastighet', 'storlek': 'Storlek', 'energi': 'Energi (i tusental)', 'antal': 'Antal'}
#: If a `.txt` file containing the data points of an average graph should be generated.
avg_tables = True
#: Title format of a run graph.
run_title_format = 'KEY, körning RUN'
#: File name format of a run graph.
run_fname_format = 'RUN, KEY'
#: Title format of an average graph.
avg_title_format = 'KEY, medelvärde'
#: File name format of an average graph.
avg_fname_format = 'KEY, medelvärde'
#: File name format of an average graph table file.
avg_table_fname_format = 'KEY'
#: Data format of an average graph table file.
avg_table_data_format = 'X,Y'
#: Delete non-statistics files after making the graphs.
remove_non_statistics = True

############gui############

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

############spreadsheet############

#: Enables spreadsheet.exe to be run from :mod:`graph`.
#: This does not mean it can't be run manually though!
enable_spreadsheet = True
#: ``.txt`` files to make table(s) out of.
to_queue = ('val1', 'val2', 'hastighet', 'storlek')
#: Variables to use in the tables.
spreadsheet_vars = ('hastighet', 'storlek')
#: Title of the spreadsheet x column.
spreadsheet_x_column = 'Tid (m)'
#: The main spreadsheet format for title cells (other cells have formats instantiated at runtime)
spreadsheet_format = {'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#399ee6'}

############simulation############

#: The format of the simulation directory.
dir_format = '%a %H.%M, %d %b'
#: Name of the main executable file.
exe = 'startworld.exe'
#: How many times the program is run.
runs = 10
#: In seconds, the duration of each run.
duration = 1800
