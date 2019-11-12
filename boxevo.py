import pygame as pg

from game_setup import startup, get_screen, draw_border
from sprite import EntityGroup, FoodGroup, MarkerSpriteGroup

from importlib.machinery import SourceFileLoader

cfg = SourceFileLoader('config', './config.py').load_module()


def main():
    startup()
    entities = EntityGroup()
    foods = FoodGroup()
    birth_markers = MarkerSpriteGroup(cfg.birth_marker_duration, cfg.birth_marker_color)
    death_markers = MarkerSpriteGroup(cfg.death_marker_duration, cfg.death_marker_color)

    entities.populate(placement=None,
                      energy=cfg.start_energy,
                      speed=cfg.start_speed,
                      size=cfg.start_size,
                      birth_marker_group=birth_markers)

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        get_screen().fill((0, 0, 0))
        draw_border()

        foods.spawn()
        entities.loop(entities=entities, foods=foods, birth_marker_group=birth_markers, death_marker_group=death_markers)
        birth_markers.loop()
        death_markers.loop()

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
