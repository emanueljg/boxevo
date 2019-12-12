"""This module is for config retrieval and syntactic sweetened handling of the values."""

from random import random
from os import path, getcwd
from importlib.machinery import SourceFileLoader



def get_cfg():
    """Retrieve the config by importing it as a module at runtime.

    Called at module level for most modules.
    """
    # Set the correct path depending on if it's creating documentation or running.
    pth = '../config.py' if path.basename(getcwd()) == 'docs' else './config.py'

    return SourceFileLoader('config', pth).load_module()


def formula(f, **kwargs) -> float:
    """Evaluate a function in a string format by variable substitution.

    :param f: Func with 0 or more placeholders (speed, size, energy, etc.) that are substituted dynamically.
    :type f: str
    :param kwargs: The keys are the name of the placeholder, values are the replacements.
    :type kwargs: dict, optional
    :return: The evaluated value after substitution
    :rtype: float
    """
    for k, v in kwargs.items():
        f = f.replace(str(k), str(v))
    return eval(f)


def prob(value) -> bool:
    """Probability evaluation in decimal form as dice roll.

    :param value: The upper bounds of the dice roll.
    :type value: float
    :return: The dice roll result.
    :rtype: bool
    """
    return True if random() < value else False
