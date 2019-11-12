import pygame as pg

from os import environ
from random import random
from win32api import WinExec

from importlib.machinery import SourceFileLoader

cfg = SourceFileLoader('config', './config.py').load_module()


def startup():
    pg.init()
    environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, cfg.window_roof_offset)

    if cfg.manual_dims is None:
        info = pg.display.Info()
        pg.display.set_mode((info.current_w, info.current_h - cfg.window_roof_offset - cfg.window_floor_offset))
    else:
        pg.display.set_mode((cfg.manual_dims[0], cfg.manual_dims[1] - cfg.window_roof_offset - cfg.window_floor_offset))

    if cfg.auto_start_scatter: WinExec('scatter.exe')


def get_screen():
    return pg.display.get_surface()


def draw_border():
    width, height = get_screen().get_size()
    return pg.draw.rect(get_screen(),
                        cfg.border_color,
                        (cfg.border_left_offset,
                         cfg.border_roof_offset,
                         width * cfg.border_width_factor,
                         height * cfg.border_height_factor),
                        cfg.border_thick)


def prob(f, x):
    f = f.replace('x', str(x))
    chance = eval(f)
    dice = random()
    return True if dice < chance else False


def formula(f, **kwargs):
    for k, v in kwargs.items():
        f = f.replace(str(k), str(v))

    return eval(f)


