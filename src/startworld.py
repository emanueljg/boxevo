"""Start the 2D-evolution environment and populate it with sprites.

This can be run by both itself and ``simulate.py``, for multiple tests.

Almost all of the GUI functionality is abstracted away either by `PyGame <https://www.pygame.org>` or :mod:`gui`,
leaving space for all of the project-specific logic.

Almost all of the runtime behaviour for this module and all others are made unique by the :mod:`config`.
"""

import pygame as pg
from timeit import default_timer as timer
from sys import argv

from src.config_handling import get_cfg
from src.gui import prep, get_screen, draw_border
from src.sprite import EntityGroup, FoodGroup, MarkerGroup

cfg = get_cfg()


def main():
    """Main function containing the event loop.

    All of the :mod:`sprite` objects and its groups are instantiated here.

    The main event loop is set to run at a constant pace of 60 frames per second but
    because of bottlenecks (mainly rendering), the actual game speed will slow down as more
    :class:`sprite.Entity` objects become active.

    "Actions" of the :class:`sprite.Entity` (such as :meth:`sprite.Entity.move`) and other :mod:`sprite` subclasses
    are carried out by calling their respective group's ``loop`` method, which in their turn
    call each of the individual sprite's ``update`` method.
    See: :meth:`sprite.EntityGroup.loop` and :meth:`sprite.Entity.update`.
    """
    run = None if len(argv) == 1 else argv[1]

    prep()
    entities = EntityGroup()
    foods = FoodGroup()
    birth_markers = MarkerGroup(cfg.birth_marker_duration, cfg.birth_marker_color)
    starve_markers = MarkerGroup(cfg.starve_marker_duration, cfg.starve_marker_color)

    entities.populate(placement=None,
                      birth_marker_group=birth_markers)

    clock = pg.time.Clock()

    start_time = timer()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        get_screen().fill((0, 0, 0))
        draw_border()

        foods.spawn()
        entities.loop(run=run,
                      elapsed=round((timer()-start_time)),
                      entity_group=entities,
                      food_group=foods,
                      birth_marker_group=birth_markers,
                      starve_marker_group=starve_markers)

        birth_markers.loop()
        starve_markers.loop()

        pg.display.flip()
        clock.tick(cfg.fps)


if __name__ == "__main__":
    main()
