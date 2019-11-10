import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import psutil
import sys

from time import sleep

from game_setup import get_vars


class Scatter:
    old_values = []
    counter = 0

    fig, ax = plt.subplots()
    x, y = [], []
    source_x, source_y = [], []
    sc = ax.scatter(x, y)

    vars = get_vars('constants.yaml')['statistics']
    kill_on_main_exit = vars['kill_on_main_exit']
    old_values_timer = vars['old_values_timer']
    pause_timer = vars['pause_timer']


def animate(i):

    if Scatter.kill_on_main_exit and 'pyvolution' not in (p.name() for p in psutil.process_iter()):
        sys.exit()

    if Scatter.counter + 1 > len(Scatter.source_x):
        Scatter.counter = 0

    if Scatter.counter == 0:
        if i != 0:
            sleep(Scatter.pause_timer)  # We don't want to sleep right when starting the program!

        while True:
            with open('values.txt', 'r') as f:
                values = f.readlines()
            if Scatter.old_values == values:
                sleep(Scatter.old_values_timer)  # Wait until we get new vales
            else:
                break

        Scatter.x.clear()
        Scatter.y.clear()
        Scatter.source_x.clear()
        Scatter.source_y.clear()

        for value in values:
            x_val, y_val = value.split(',')
            Scatter.source_x.append(x_val)
            Scatter.source_y.append(y_val)

        plt.xlim(0, int(max([int(i) for i in Scatter.source_x]) + 2))
        plt.ylim(0, int(max([int(i) for i in Scatter.source_y]) + 2))

        Scatter.old_values = values

    Scatter.x.append(Scatter.source_x[Scatter.counter])
    Scatter.y.append(Scatter.source_y[Scatter.counter])
    Scatter.sc.set_offsets(np.c_[Scatter.x, Scatter.y])

    Scatter.counter += 1


def main():
    ani = matplotlib.animation.FuncAnimation(Scatter.fig, animate, interval=1, repeat=True)
    plt.show()


main()
