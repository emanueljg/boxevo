"""This module is for config retrieval and syntactic sweetened handling of the values."""

import random
from os import path, getcwd
from sys import exit, argv
from importlib.machinery import SourceFileLoader
from typing import Union


def get_cfg():
    """Retrieve the config by importing it as a module at runtime.

    This should be called at the top of the relevant files. Depending on the current working directory,
    it will magically adjust the path to the config:

    * ``cwd == 'docs:': pth = '../'`` triggers for compilation of documentation with Sphinx.
    * ``cwd == 'simulation': pth = 'bundle'`` triggers for config fetching in ``simulate.py``.

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
        print(f'ERROR: "{argv[0]}" could not find or reach config.py from current working directory "{getcwd()}".')


def formula(f, **kwargs) -> Union[int, float]:
    """Evaluate a function in a string format by variable substitution.

    :param f: Function with 0 or more placeholders (``speed``, ``size``, ``energy``, etc.) that are substituted dynamically.
    :type f: str
    :param kwargs: The keys are the name of the placeholder, values are the replacements.
    :type kwargs: int or float, optional
    :return: The evaluated value after substitution.
    :rtype: int or float
    """
    for k, v in kwargs.items():
        f = f.replace(str(k), str(v))
    return eval(f)


def prob(value) -> bool:
    """Probability evaluation.

    :param value: The probability.
    :type value: float
    :return: Result of the evaluation.
    :rtype: bool
    """
    return random.random() < value
