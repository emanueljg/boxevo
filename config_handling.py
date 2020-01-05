"""This module is for config retrieval and syntactic sweetened handling of the values."""

from random import random
from os import path, getcwd
from sys import exit, argv
from importlib.machinery import SourceFileLoader


def get_cfg():
    """Retrieve the config by importing it as a module at runtime.

    Should be called at the top of the relevant files, module-level. Depending on the cwd,
    it will magically adjust the path to the config:

    ``cwd == 'docs:': pth = '../'`` will be true for compilation of documentation with Sphinx.
    ``cwd == 'simulation': pth = 'bundle'`` will be true for cfg fetching in ``simulate.py``.

    If these checks fail, path is set to the current working directory, i.e. ``'./'``.
    """
    cwd = path.basename(getcwd())
    pth = None

    if cwd == 'docs':
        pth = '../'
    elif cwd == 'simulation':
        pth = 'bundle'
    else:
        pth = './'

    try:
        return SourceFileLoader('config', path.join(pth, 'config.py')).load_module()
    except FileNotFoundError:
        exit(f'ERROR: "{path.basename(argv[0])}" could not find or reach config.py from current working directory "{cwd}".'
             '\nExiting...')


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
    """Probability evaluation in decimal form as a "dice roll".

    :param value: The upper bounds of the dice roll.
    :type value: float
    :return: The dice roll result.
    :rtype: bool
    """
    return random() < value
