
import yaml

import pygame as pg
from os import environ
from random import random


def get_vars(path):
    with open(path, 'r') as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as e:
            print(e)


vars = get_vars('constants.yaml')['screen']

window_roof_offset = vars['window_roof_offset']
window_floor_offset = vars['window_floor_offset']

border_roof_offset = vars['border_roof_offset']
border_left_offset = vars['border_left_offset']
border_width_factor = vars['border_width_factor']
border_height_factor = vars['border_height_factor']
border_thick = vars['border_thick']
border_color = vars['border_color']




def startup(manual_dims):
    pg.init()
    environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, window_roof_offset)  # UPPERWINDOW

    if manual_dims is None:
        info = pg.display.Info()
        pg.display.set_mode((info.current_w, info.current_h - window_roof_offset - window_floor_offset))
    else:
        pg.display.set_mode((manual_dims[0], manual_dims[1] - window_roof_offset - window_floor_offset))


def get_screen():
    return pg.display.get_surface()


def draw_border():
    width, height = get_screen().get_size()
    return pg.draw.rect(get_screen(),
                        border_color,
                        (border_left_offset, border_roof_offset, width * border_width_factor, height*border_height_factor),
                        border_thick)


# def GRAPH_RECT():
#    return pg.draw.rect(get_screen(),
#                        border_color,
#                        (width * border_width_factor+ 50, bor, 300, height * 0.3), BORDERTHICK)


def prob(f, x):
    f = f.replace('x', str(x))
    chance = eval(f)
    dice = random()
    return True if dice < chance else False


def formula(f, **kwargs):

    for k, v in kwargs.items():
        f = f.replace(str(k), str(v))

    return eval(f)


