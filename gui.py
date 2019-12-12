"""This module handles abstracted-away gui methods related to PyGame."""


import pygame as pg
from os import environ

from config_handling import get_cfg

cfg = get_cfg()


def prep():
    """Initial preparations for the main window.

    Dimensions will be manually or dynamically set depending on ``config.py``.
    """
    pg.init()
    environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, cfg.window_roof_offset)

    if cfg.manual_dims is None:
        info = pg.display.Info()
        pg.display.set_mode((info.current_w,
                             info.current_h - cfg.window_roof_offset - cfg.window_floor_offset))
    else:
        pg.display.set_mode((cfg.manual_dims[0],
                             cfg.manual_dims[1] - cfg.window_roof_offset - cfg.window_floor_offset))



def get_screen() -> pg.Surface:
    """Get the PyGame display surface.

    :return: The display surface.
    :rtype: PyGame.Surface
    """
    return pg.display.get_surface()


def draw_border() -> pg.Rect:
    """Draw the PyGame border rect and return it.

    The border rect will be drawn as a border, not an opaque rectangle.

    :return: The border rect.
    """
    width, height = get_screen().get_size()
    return pg.draw.rect(get_screen(),
                        cfg.border_color,
                        (cfg.border_left_offset,
                         cfg.border_roof_offset,
                         width * cfg.border_width_factor,
                         height * cfg.border_height_factor),
                        cfg.border_thick)
