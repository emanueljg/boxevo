"""This module handles game "objects" with a visual representation - "sprites" - and all of their "actions".

.. _Sprite: https://www.pygame.org/docs/ref/sprite.html
.. _Group: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group

The sprite classes here are all subclasses of Pygame's Sprite_ class.

- :class:`Entity` handles the living creature.
- :class:`Food` handles the food.
- :class:`Marker` handles visual representation of events.

Each group has an accompanying Group in order to deal with all of the sprites as a collection (subclassing Group_):

- :class:`EntityGroup`
- :class:`FoodGroup`
- :class:`MarkerGroup`
"""

import pygame as pg

from random import randint, choice

from parsing import get_cfg, formula, prob
from gui import get_screen, draw_border

cfg = get_cfg()


class Entity(pg.sprite.Sprite):
    """Class for a living creature.

    .. _Sprite: https://www.pygame.org/docs/ref/sprite.html
    .. _Sprite.update: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.update

    A subclass of PyGame's Sprite_ class that allows for automated method calls each
    game loop iteration, "action(s)", essentially giving the sprite its *life*.
    This is done by overriding Sprite.update_, a placeholder method that is called with :meth:`EntityGroup.update`
    and its arguments. The overridden method contains all actions:
    moving, mating, eating, dying and modification of values.

    :param energy: How much energy it has, depleted each turn by a formula (from :mod:`config`) using ``speed`` and ``size``
    :type energy: int
    :param speed: How fast it moves each turn, ``self.rect.(direction) += speed``.
    :type speed: int
    :param size: How big is is, in pixels (quadratic).
    :type size: int
    :param mating_counter: To see if it can mate or not, ``counter > counter_check`` is a requirement in :meth:`mate`.
    :type mating_counter: int
    :param age_counter: Its age. Mostly used in :meth:`die` and :meth:`mate`.
    :type age_counter: int
    :param image: What it looks like. Scaled by ``size``.
    :type image: Pygame.Surface
    :param rect: The rectangle, mostly used for :meth:`move` and collision checks. Shortcut to ``self.image.get_rect()``.
    :type rect: Pygame.Rect
    """
    def __init__(self, energy, speed, size):
        """Decorator function where counters are set to 0 and image is properly set."""

        super().__init__()
        self.speed = speed
        self.size = size
        self.energy = energy
        self.mating_counter = 0
        self.age_counter = 0
        self.direction_counter = 0
        self.direction = None
        self.image = pg.transform.scale(pg.image.load(cfg.entity_image), (size, size)).convert()
        self.rect = self.image.get_rect()

    def move(self):
        """Vertical and horizontal sprite movement

        .. _Rect: https://www.pygame.org/docs/ref/rect.html#pygame.Rect

        If the condition ``direction_counter >= counter_check`` is true, choose a direction to go to and
        reset the counter.

        This works by using PyGame's Rect_ magic, incrementing "coordinate attributes" to move.
        If movement would collide with the border, the counter is set to the check value so that a new
        direction can be chosen next turn.
        """
        border = draw_border()

        if self.direction_counter >= cfg.direction_counter_roof or self.age_counter == 0:
            self.direction = choice(('up', 'down', 'left', 'right'))
            self.direction_counter = 0

        if self.direction == 'up':
            if (self.rect.y - self.speed) < border.top:
                self.direction_counter = cfg.direction_counter_roof
            else:
                self.rect.y -= self.speed

        if self.direction == 'down':
            if (self.rect.bottom + self.speed) > border.bottom:
                self.direction_counter = cfg.direction_counter_roof
            else:
                self.rect.bottom += self.speed

        if self.direction == 'left':
            if (self.rect.x - self.speed) < border.left:
                self.direction_counter = cfg.direction_counter_roof
            else:
                self.rect.x -= self.speed

        if self.direction == 'right':
            if (self.rect.right + self.speed) > border.right:
                self.direction_counter = cfg.direction_counter_roof
            else:
                self.rect.right += self.speed

    def mate(self, entity_group, birth_marker_group):
        """Mating and birth if all checks are passed.

        If a partner is found by collision check, and all of these conditions are met,

        - It and its partner has not mated recently (``mating_counter > mating_counter_roof``)
        - It and its partner is old enough (``age_counter > age_counter_roof``)
        - It and its partner has enough energy for minimal cost (``energy > cfg.mating_energy_formula_min)``)
        - It and its partner has enough energy for the parents' greatest energy cost (``energy > greater_cost``)

        then a new class instance is created. For this new class instance:

        - **Energy** is equal to ``greatest_cost * 2`` (simulating the parents giving their own share)
        - **Speed** and **Size** are equal to a mean value of the parents' values, ``+-randint(min_gene_variation, max_gene_vaiation)``

        The actual "birth" is done in :meth:`EntityGroup.populate` by calling it in this method.

        :param entity_group: Group of entities.
        :type entity_group: EntityGroup
        :param birth_marker_group: Group of birth markers.
        :type birth_marker_group: MarkerGroup
        """
        partners = pg.sprite.spritecollide(self, entity_group, dokill=False)
        if len(partners) >= 2 and prob(cfg.mating_chance):
            partner = partners[1]

            greater_cost = int(max((formula(cfg.mating_energy_formula, energy=self.energy),
                                    formula(cfg.mating_energy_formula, energy=partner.energy))))

            if self.mating_counter < cfg.mating_counter_roof or partner.mating_counter < cfg.mating_counter_roof:
                return
            elif self.age_counter < cfg.mating_age_counter_roof or partner.age_counter < cfg.mating_age_counter_roof:
                return
            elif self.energy < cfg.mating_energy_formula_min or partner.energy < cfg.mating_energy_formula_min:
                return
            elif self.energy < greater_cost or partner.energy < greater_cost:
                return
            else:
                born_speed = (self.speed + partner.speed) // 2 + (randint(*cfg.speed_variation) * choice((1, -1)))
                born_size = (self.size + partner.size) // 2 + (randint(*cfg.size_variation) * choice((1, -1)))
                if born_speed < cfg.min_speed:
                    born_speed = cfg.min_speed
                if born_size < cfg.min_size:
                    born_size = cfg.min_size

                entity_group.populate(placement=(self.rect.x, self.rect.y),
                                      birth_marker_group=birth_marker_group,
                                      energy=(2 * greater_cost),
                                      speed=born_speed,
                                      size=born_size)

                self.mating_counter, partner.mating_counter = 0, 0
                self.energy -= greater_cost
                partner.energy -= greater_cost

    def eat(self, food_group):
        """Consume food.

        Check for collisions with ``food_group``,
        kill any food sprite matches,
        give :data:`config.food_energy` for each match.

        :param food_group: Group of foods
        :type food_group: FoodGroup
        """
        foods = pg.sprite.spritecollide(self, food_group, dokill=True)
        for _ in foods:
            self.energy += cfg.food_energy

    def die(self, entity_group, starve_marker_group):
        """Die from starvation if conditions are met.

        Starve :class:`Marker` is set if death occurs.

        :param entity_group: Group of entities.
        :type entity_group: EntityGroup
        :param starve_marker_group: Group of starve markers
        :type starve_marker_group: MarkerGroup
        """
        if self.energy < 0:
            starve_marker_group.create(self)
            entity_group.remove(self)

    def modify_values(self):
        """Update all relevant attributes.

        Energy is drained with a formula that is a function of ``speed`` and ``size`` (:data:`config.energy_drain_formula`)
        Mating and age counters are incremented by 1.
        Direction counter is incremented by an integer in a random interval (:data:`config.direction_counter_increment`)
        """
        self.energy -= formula(cfg.energy_drain_formula, speed=self.speed, size=self.size)
        self.mating_counter += 1
        self.age_counter += 1
        min_incr, max_incr = cfg.direction_counter_increment
        self.direction_counter += randint(self.speed // max_incr, self.speed // min_incr)

    def update(self, entity_group, food_group, birth_marker_group, starve_marker_group):
        """Carry out all the actions in a turn.

        :param entity_group: Group of entities.
        :type entity_group: EntityGroup
        :param food_group: Group of foods.
        :type food_group: FoodGroup
        :param birth_marker_group: Group of birth markers.
        :type birth_marker_group: MarkerGroup
        :param starve_marker_group: Group of starve markers.
        :type starve_marker_group: MarkerGroup
        """
        self.move()
        self.mate(entity_group, birth_marker_group)
        self.eat(food_group)
        self.die(entity_group, starve_marker_group)
        self.modify_values()


class EntityGroup(pg.sprite.Group):
    """Container group for :class:`Entity`.

    .. _Group: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group

    This container is a  subclass of Pygame's Group_.
    It handles birth in :meth:`populate` and file saving in :meth:`save_to_file` for statistic purpouses.
    :meth:`loop` is called each turn, calling :meth:`Entity.update`, :meth:`save_to_file` and drawing the sprites.
    """
    def __init__(self):
        """Constructor method"""
        super().__init__()
        self.statistics_counter = 0

    def populate(self, placement, birth_marker_group, **kwargs):
        """Add ``n`` new Entity instance(s) to the group.

        This method is called for both "program-start" birth ``placement = None, n = 1``
        and birth by parents ``placement = (x, y), n != 1``.
        Birth is marked by :class:`Marker`.

        :param placement: The coordinates of the new entity. If `None`, randomly set to within the border rect.
        :type placement: Union[tuple, None]
        :param energy: The energy of the new instance.
        :type energy: int
        :param birth_marker_group: Group of birth markers
        :type birth_marker_group: MarkerGroup
        :param kwargs: Passes other parameters to :class:`Entity`, such as ``speed`` and ``size``.
        :type kwargs: int, optional
        """
        n = 1 if placement is not None else cfg.start_amount

        for _ in range(n):
            entity = Entity(cfg.start_energy,
                            randint(*cfg.start_speed),
                            randint(*cfg.start_size)) if placement is None else Entity(**kwargs)

            border = draw_border()
            if placement is None:
                entity.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
            else:
                entity.rect.center = (placement[0], placement[1])

            self.add(entity)
            birth_marker_group.create(entity)

    def save_to_file(self, run, elapsed):
        """Save attributes of all entities to file, only triggered if ``statistics_counter`` passes the check.

        :param run: What run the program is on. Will be ``None`` if program is not called from ``simulate.py``.
        :type run: int or None
        :param elapsed: In seconds, how long since the program started.
        :type elapsed: int
        """
        self.statistics_counter += 1

        if self.statistics_counter == cfg.statistics_counter_roof:
            speeds = [entity.speed for entity in self]
            sizes = [entity.size for entity in self]
            energy = [entity.energy for entity in self]
            amount = len(self)

            speedavg = sum(speeds) // len(speeds)
            sizeavg = sum(sizes) // len(sizes)
            energyavg = int(sum(energy) // len(energy))

            fname = 'val.txt' if run is None else f'val{run}.txt'

            with open(fname, 'a') as f:
                f.write(f'{elapsed}:|'
                        f'speed={speedavg}|'
                        f'size={sizeavg}|'
                        f'energy={energyavg}|'
                        f'amount = {amount}|'
                        '\n')

            self.statistics_counter = 0

    def loop(self, run, elapsed, entity_group, food_group, birth_marker_group, starve_marker_group):
        """Looping method called each game turn.

        This method does three things:

        - Call each of the entities' ``update()`` method to do their actions (:meth:`Entity.update`).
        - Save their attributes to file with :meth:`save_to_file`.
        - Draw them on the screen.

        :param run: What run the program is on. Will be ``None`` if program is not called from ``simulate.py``.
        :type run: int or None
        :param elapsed: In seconds, how long since the program started.
        :type elapsed: int
        :param entity_group: Group of entities.
        :type entity_group: EntityGroup
        :param food_group: Group of foods.
        :type food_group: FoodGroup
        :param birth_marker_group: Group of birth markers.
        :type birth_marker_group: MarkerGroup
        :param starve_marker_group: Group of starve markers.
        :type starve_marker_group: MarkerGroup
        """
        # TODO update docs
        self.update(entity_group, food_group, birth_marker_group, starve_marker_group)
        self.save_to_file(run, elapsed)
        self.draw(get_screen())


class Food(pg.sprite.Sprite):
    """Class for a food object.

    .. _Sprite: https://www.pygame.org/docs/ref/sprite.html
    .. _Group: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group

    This is a subclass of PyGame's Sprite_ class, but much simpler than :class:`Entity`.
    Its only purpose is be spawned by its PyGame Group_ (:class:`FoodGroup`) and eaten by an :class:`Entity`.

    :param image: What it looks like. Scaled by ``size``.
    :type image: Pygame.Surface
    :param rect: The rectangle representation of ``image``. Shortcut to ``self.image.get_rect()``.
    :type rect: Pygame.Rect
    """
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(cfg.food_image), (cfg.food_size, cfg.food_size)).convert()
        self.rect = self.image.get_rect()


class FoodGroup(pg.sprite.Group):
    """Container group for :class:`Food`

    .. _Group: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group

    This container is a subclass of Pygame's Group_. Mainly of importance to spawn in the food.

    :param spawn_counter: Counts up to :data:`config.food_spawn_counter_roof` by random integer in interval :data:`config.food_spawn_counter_increment`.
    :type spawn_counter: int
    """
    def __init__(self):
        super().__init__()
        self.spawn_counter = 0

    def spawn(self):
        """Spawn :data:`config.food_amount` amount of food.

        Similar to :meth:`Entity.populate` but much simpler.
        """
        if self.spawn_counter >= cfg.food_spawn_counter_roof:
            for _ in range(cfg.food_amount):
                food = Food()
                border = draw_border()
                food.rect.center = (randint(border.left, border.right), randint(border.top, border.bottom))
                self.add(food)
            self.spawn_counter = 0
        else:
            self.spawn_counter += randint(*cfg.food_spawn_counter_increment)

        self.draw(get_screen())


class Marker(pg.sprite.Sprite):
    """Marker for certain events.

    .. _Sprite: https://www.pygame.org/docs/ref/sprite.html

    A subclass of Pygame's Sprite_ class which is instantiated after certain event,
    in order to visually clarify when something occurs.
    This is showed as a simple colored square (color indicates type of event),
    that disappears after ``duration_counter == duration_counter_roof``

    Current valid events:

    - **starve**: die of lack of energy
    - **birth**: be instantiated

    :param marked_sprite: The marked Sprite_, used to inherit the dimensions and placement.
    :type marked_sprite: Pygame.Sprite
    :param duration_counter: Elapsed duration.
    :type duration_counter: int
    :param duration_counter_roof: When ``duration_counter == duration_counter_roof``, the marker is removed.
    :type duration_counter_roof: int
    :param color: (R, G, B) color of the image.
    :type color: tuple
    :param image: What it looks like (single-color) . Scaled by ``marked_sprite.size``.
    :type image: Pygame.Rect
    :param rect: The rectangle representation of the class. Equivalent of ``self.image`` in this particular class.
    :type rect: Pygame.Rect
    """
    def __init__(self, marked_sprite, duration_counter_roof, color):
        """Constructor method."""
        super().__init__()
        self.marked_sprite = marked_sprite
        self.duration_counter = 0
        self.duration_counter_roof = duration_counter_roof
        self.image = pg.Surface((self.marked_sprite.size, self.marked_sprite.size))
        self.rect = self.image.fill(color)
        self.rect.center = (self.marked_sprite.rect.x, self.marked_sprite.rect.y)

    def update(self):
        """Check if ``duration_counter == duration_counter_roof``, and kill itself if it is."""
        self.duration_counter += 1
        if self.duration_counter == self.duration_counter_roof:
            self.kill()


class MarkerGroup(pg.sprite.Group):
    """Group container for :class:`Marker`.

    :param duration_counter_roof: When ``duration_counter == duration_counter_roof, the marker is removed.``
    :type duration_counter_roof: int
    :param color: Color of the image.
    :type color: tuple
    """
    def __init__(self, duration_counter_roof, color):
        super().__init__()
        self.duration_counter_roof = duration_counter_roof
        self.color = color

    def create(self, marked_sprite):
        """Create and add a new marker to the container.

        :param marked_sprite: The marked sprite in question, used to inherit dimensions and placement of the marker.
        :type marked_sprite: Pygame.Sprite
        """
        self.add(Marker(marked_sprite, self.duration_counter_roof, self.color))

    def loop(self):
        """Looping method called each turn, updates markers and draws them to the screen."""
        self.update()
        self.draw(get_screen())
