from game_setup import get_screen, draw_border, get_vars, prob, formula

import pygame as pg
from random import randint


class Entity(pg.sprite.Sprite):
    """Class for the game entity, subclassing Sprite with useful methods."""

    def __init__(self, imgpath, energy, speed, size):
        super().__init__()
        pre_img = pg.image.load(imgpath if ".png" in imgpath else (imgpath + ".png"))
        self.image = pg.transform.scale(pre_img, (size, size)).convert()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.size = size
        self.energy = energy
        self.mating = 0
        self.age = 0
        self.direction = None
        self.direction_counter = 0

    def chillout(self):
        self.mating = 0

    def note_death(self):
        pass

    def update(self,
               entities,
               foods,
               mating_requirement,
               mating_energy,
               mating_age_requirement,
               gene_variation,
               energy_food,
               direction_roof,
               direction_speed_decrement,
               old_death,
               old_age_formula,
               energy_drain_formula,
               mating_chance):
        """ Method that contains all of the entities actions in a turn.
        Mate: Requires two partners, offspring will me (par + par)/2 +(-) variance
        Eat: Get energy from food.
        Move: Choose a random direction, walk in said direction until you get bored of it.
              Boredom factor is a function of speed (it has to be).
        Count down: (de/in)-crement relevant values.

        """

        if self.speed <= 0: self.speed = 1  # Correct for bad speed values.

        # Mate
        partners = pg.sprite.spritecollide(self, entities, dokill=False)
        if len(partners) == 2:
            if prob('x', mating_chance):
                partner = partners[1]
                if self.mating < mating_requirement or partner.mating < mating_requirement:
                    pass
                elif self.energy < mating_energy or partner.energy < mating_energy:
                    pass
                elif self.age < mating_age_requirement or partner.age < mating_age_requirement:
                    pass
                else:
                    medianspeed = (partner.speed + self.speed) // 2
                    mediansize = (partner.size + self.size) // 2
                    speedmin = 1 if medianspeed - gene_variation < 0 else medianspeed - gene_variation
                    sizemin = 1 if mediansize - gene_variation < 0 else mediansize - gene_variation
                    entities.populate(placement=(self.rect.x, self.rect.y),
                                      image="optimusfly",
                                      energy=get_vars('constants.yaml')['entity']['start_energy'],
                                      speed=(speedmin, medianspeed + gene_variation),
                                      size=(sizemin, mediansize + gene_variation))
                    self.chillout()
                    self.energy -= mating_energy
                    partner.chillout()
                    partner.energy -= mating_energy

        # Eat
        foods = pg.sprite.spritecollide(self, foods, dokill=True)
        for food in foods:
            self.energy += energy_food

        # Move
        border = draw_border()
        choice = randint(1, 4)
        if self.direction_counter <= 0:
            self.direction = None
            self.direction_counter = direction_roof

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

        # Count down
        self.energy -= formula(energy_drain_formula, x=self.speed, y=self.size)
        self.mating += 1
        self.age += 1
        dir_a, dir_b = direction_speed_decrement
        self.direction_counter -= randint(self.speed // dir_b + 1, self.speed // dir_a + 1)

        # Starve
        if self.energy < 0:
            entities.remove(self)

        # Chance of dying of old age
        if prob(old_age_formula, self.age):
            entities.remove(self)


class Food(pg.sprite.Sprite):

    def __init__(self, imgpath, size):
        super().__init__()
        pre_img = pg.image.load(imgpath if ".png" in imgpath else (imgpath + ".png"))
        self.image = pg.transform.scale(pre_img, size).convert()
        self.rect = self.image.get_rect()


class StartGroup(pg.sprite.Group):
    def __init__(self, n, sprite_cls):
        super().__init__()
        self.n = n
        self.sprite_cls = sprite_cls
        self.noting_counter = 0

    def populate(self, placement, image, energy, **weighted_kwargs):
        """ Spawn n entities with varying amounts of randomness.
        Used both for initial spawning and for mating-spawning.
        """
        n = 1 if placement is not None else self.n
        for _ in range(n):
            kwargs = {k: randint(v[0], v[1]) for k, v in weighted_kwargs.items()}
            s = self.sprite_cls(image, energy, **kwargs)
            border = draw_border()
            if placement is None:
                s.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
            else:
                s.rect.center = (placement[0], placement[1])

            self.add(s)

    def loop(self,
             entities,
             foods,
             mating_requirement,
             mating_energy,
             mating_age_requirement,
             gene_variation,
             energy_food,
             direction_roof,
             direction_speed_decrement,
             old_death,
             old_age_formula,
             energy_drain_formula,
             mating_chance,
             noting_counter,
             ):
        """ Wrapper method for .update() in order to include rendering, .draw()"""

        self.update(entities,
                    foods,
                    mating_requirement,
                    mating_energy,
                    mating_age_requirement,
                    gene_variation,
                    energy_food,
                    direction_roof,
                    direction_speed_decrement,
                    old_death,
                    old_age_formula,
                    energy_drain_formula,
                    mating_chance)

        self.draw(get_screen())

        if self.noting_counter == noting_counter:
            with open('values.txt', 'w') as noting_file:
                noting_file.seek(0)
                noting_file.truncate()
                speeds = [str(entity.speed) for entity in self]
                sizes = [str(entity.size) for entity in self]
                for speed, size in zip(speeds, sizes):
                    noting_file.writelines(f'{speed},{size}\n')

            self.noting_counter = 0

        self.noting_counter += 1


class BurstGroup(pg.sprite.Group):
    """Class for sprites that spawn each time in a given interval.

    Synonymous with "food class group"
    """

    def __init__(self, sprite_cls, n, burst, increment):
        super().__init__()
        self.sprite_cls = sprite_cls
        self.n = n
        self.burst = burst
        self.burst_counter = 0
        self.increment = increment

    def burst_out(self, **kwargs):
        """ Similar to StartGroup.populate() but is called every "turn". """
        if self.burst_counter >= self.burst:
            for _ in range(self.n):
                s = self.sprite_cls(**kwargs)
                border = draw_border()
                s.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
                self.add(s)
            self.burst_counter = 0
        else:
            self.burst_counter += randint(*self.increment)

        self.draw(get_screen())
