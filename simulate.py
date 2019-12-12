from win32process import CreateProcess, STARTUPINFO
from time import strftime, time, sleep
from os import path, mkdir, makedirs, remove, system, listdir
from shutil import copy2, SameFileError

from config_handling import get_cfg

cfg = get_cfg()


def main():
    current = strftime(cfg.time_dir_format)
    makedirs(path.join(current, cfg.statistics_dir), exist_ok=True)

    for run in range(1, cfg.runs + 1):

        makedirs(str(run))

        programs = (cfg.main_executable, cfg.statistics_executable)

        for to_copy in listdir('bundle'):
            try:
                copy2(to_copy, path.join(current, str(run)))
            except SameFileError:
                pass

        due = time() + cfg.duration

        for program in programs:
            CreateProcess(None,
                          path.join(current, str(run), program),
                          None,
                          None,
                          False,
                          0,
                          None,
                          path.join(current, str(run)),
                          STARTUPINFO())

        while True:
            if time() > due:
                system(f'TASKKILL /F /IM {cfg.main_executable} & TASKKILL /F /IM {cfg.statistics_executable}')
            sleep(1)


if __name__ == '__main__':
    main()




