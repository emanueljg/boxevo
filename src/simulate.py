"""This module runs :mod:`startworld` multiple times and graphs gathered data using :mod:`graph`."""
from win32process import CreateProcess, STARTUPINFO
from time import strftime, time, sleep
from os import path, mkdir, system, listdir
from shutil import copy2, SameFileError

from src.config_handling import get_cfg

cfg = get_cfg()


def main():
    """Run the simulation."""
    current = strftime(cfg.dir_format)
    mkdir(current)

    for to_copy in listdir('bundle'):
        try:
            copy2(path.join('bundle', to_copy), current)
        except SameFileError:
            pass

    for run in range(1, cfg.runs + 1):
        CreateProcess(None, f'{path.join(current, cfg.exe)} {run}', None, None, False, 0, None, current, STARTUPINFO())
        due = time() + cfg.duration
        while True:
            if time() > due:
                system(f'TASKKILL /F /IM {cfg.exe}')
                break
            sleep(1)

    CreateProcess(None, path.join(current, "graph.exe"), None, None, False, 0, None, current, STARTUPINFO())


if __name__ == '__main__':
    main()




