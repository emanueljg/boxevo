import pygame as pg
from win32api import WinExec

from game_setup import startup, get_screen, draw_border, get_vars
from entity import Entity, Food, StartGroup, BurstGroup


def main():

    vars = get_vars('constants.yaml')

    startup(vars['screen']['manual_dims'])

    entity_vars = vars['entity']
    food_vars = vars['food']

    entities = StartGroup(n=entity_vars['start_amount'],
                          sprite_cls=Entity)

    entities.populate(placement=None,
                      image=entity_vars['image'],
                      energy=entity_vars['start_energy'],
                      speed=entity_vars['start_speed'],
                      size=entity_vars['start_size']
                      )

    foods = BurstGroup(sprite_cls=Food,
                       n=food_vars['amount'],
                       burst=food_vars['burst'],
                       increment=food_vars['burst_counter'])

    if vars['statistics']['auto_start_scatter']: WinExec('scatter.exe')

    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        get_screen().fill((0, 0, 0))
        border = draw_border()
        # r = GRAPH_RECT()

        entities.loop(entities=entities,
                      foods=foods,
                      mating_requirement=entity_vars['mating_requirement'],
                      mating_energy=entity_vars['mating_energy'],
                      mating_age_requirement=entity_vars['mating_age_requirement'],
                      gene_variation=entity_vars['gene_variation'],
                      energy_food=entity_vars['energy_food'],
                      direction_roof=entity_vars['direction_roof'],
                      direction_speed_decrement=entity_vars['direction_speed_decrement'],
                      old_death=entity_vars['old_death'],
                      old_age_formula=entity_vars['old_age_formula'],
                      energy_drain_formula=entity_vars['energy_drain_formula'],
                      mating_chance=entity_vars['mating_chance'],
                      noting_counter=vars['statistics']['noting_counter'],
                      )

        foods.burst_out(imgpath=food_vars['image'], size=food_vars['size'])
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
