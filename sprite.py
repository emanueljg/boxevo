import pygame as pg
from random import randint

from game_setup import get_screen, draw_border, prob, formula
from importlib.machinery import SourceFileLoader

cfg = SourceFileLoader('config', './config.py').load_module()


class Entity(pg.sprite.Sprite):
    def __init__(self, energy, speed, size):
        super().__init__()
        pre_img = pg.image.load(cfg.entity_image)
        self.image = pg.transform.scale(pre_img, (size, size)).convert()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.size = size
        self.energy = energy
        self.mating = 0
        self.age = 0
        self.direction = None
        self.direction_counter = 0

    def move(self):
        border = draw_border()
        if self.speed <= 0: self.speed = 1

        if self.direction_counter <= 0:
            self.direction = None
            self.direction_counter = cfg.direction_roof

        if self.direction is None:
            self.direction = randint(1, 4)

        # UP
        if self.direction == 1:
            if (self.rect.y - self.speed) < border.top:
                self.direction_counter = 0
            else:
                self.rect.y -= self.speed

        # DOWN
        if self.direction == 2:
            if (self.rect.bottom + self.speed) > border.bottom:
                self.direction_counter = 0
            else:
                self.rect.bottom += self.speed

        # LEFT
        if self.direction == 3:
            if (self.rect.x - self.speed) < border.left:
                self.direction_counter = 0
            else:
                self.rect.x -= self.speed

        # RIGHT
        if self.direction == 4:
            if (self.rect.right + self.speed) > border.right:
                self.direction_counter = 0
            else:
                self.rect.right += self.speed

    def mate(self, entities):
        partners = pg.sprite.spritecollide(self, entities, dokill=False)
        if len(partners) == 2:
            if prob('x', cfg.mating_chance):
                partner = partners[1]

                greater_cost = max((formula(cfg.mating_energy_formula, x=self.energy),
                         formula(cfg.mating_energy_formula, x=partner.energy)))

                if self.mating < cfg.mating_counter or partner.mating < cfg.mating_counter:
                    return
                elif self.age < cfg.mating_age_req or partner.age < cfg.mating_age_req:
                    return
                elif self.energy < cfg.mating_energy_formula_min or partner.energy < cfg.mating_energy_formula_min:
                    return
                elif greater_cost > self.energy or greater_cost > partner.energy:
                    return
                else:
                    medianspeed = (partner.speed + self.speed) // 2
                    mediansize = (partner.size + self.size) // 2
                    speedmin = 1 if medianspeed - cfg.gene_variation < 0 else medianspeed - cfg.gene_variation
                    sizemin = 1 if mediansize - cfg.gene_variation < 0 else mediansize - cfg.gene_variation
                    entities.populate(placement=(self.rect.x, self.rect.y),
                                      energy=(2 * greater_cost),
                                      speed=(speedmin, medianspeed + cfg.gene_variation),
                                      size=(sizemin, mediansize + cfg.gene_variation))
                    self.mating, partner.mating = 0, 0
                    self.energy -= greater_cost
                    partner.energy -= greater_cost

    def eat(self, foods):
        foods = pg.sprite.spritecollide(self, foods, dokill=True)
        for _ in foods:
            self.energy += cfg.food_energy

    def die(self, entities):
        if self.energy < 0:
            entities.remove(self)
        elif prob(cfg.old_age_formula, self.age):
            entities.remove(self)

    def modify_values(self):

        self.energy -= formula(cfg.energy_drain_formula, x=self.speed, y=self.size)
        self.mating += 1
        self.age += 1
        dir_a, dir_b = cfg.direction_speed_decrement
        self.direction_counter -= randint(self.speed // dir_b + 1, self.speed // dir_a + 1)

    def update(self, entities, foods):
        self.move()
        self.mate(entities)
        self.eat(foods)
        self.die(entities)
        self.modify_values()


class EntityGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.noting = 0

    def populate(self, placement, energy, **weighted_kwargs):
        n = 1 if placement is not None else cfg.start_amount

        for _ in range(n):
            kwargs = {k: randint(v[0], v[1]) for k, v in weighted_kwargs.items()}
            entity = Entity(energy, **kwargs)
            border = draw_border()
            if placement is None:
                entity.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
            else:
                entity.rect.center = (placement[0], placement[1])

            self.add(entity)

    def note_entities(self):
        if self.noting == cfg.noting_counter:
            with open('values.txt', 'w') as noting_file:
                noting_file.seek(0)
                noting_file.truncate()
                speeds = [str(entity.speed) for entity in self]
                sizes = [str(entity.size) for entity in self]
                for speed, size in zip(speeds, sizes):
                    noting_file.writelines(f'{speed},{size}\n')

            self.noting = 0

        self.noting += 1

    def loop(self, entities, foods):
        self.update(entities, foods)
        self.note_entities()
        self.draw(get_screen())


class Food(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pre_img = pg.image.load(cfg.food_image)
        self.image = pg.transform.scale(pre_img, (cfg.food_size, cfg.food_size)).convert()
        self.rect = self.image.get_rect()


class FoodGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.burst_counter = 0

    def spawn(self):
        if self.burst_counter >= cfg.food_counter:
            for _ in range(cfg.food_amount):
                food = Food()
                border = draw_border()
                food.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
                self.add(food)
            self.burst_counter = 0
        else:
            self.burst_counter += randint(*cfg.food_spawn_increment)

        self.draw(get_screen())
