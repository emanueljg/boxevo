import pygame as pg

from game_setup import startup, get_screen, draw_border
from sprite import EntityGroup, FoodGroup

from importlib.machinery import SourceFileLoader

cfg = SourceFileLoader('config', './config.py').load_module()


def main():
    startup()
    entities, foods = EntityGroup(), FoodGroup()

    entities.populate(placement=None,
                      energy=cfg.start_energy,
                      speed=cfg.start_speed,
                      size=cfg.start_size)

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        get_screen().fill((0, 0, 0))
        draw_border()

        foods.spawn()
        entities.loop(entities=entities, foods=foods)

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
