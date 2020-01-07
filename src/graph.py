"""This module handles variable graphing using `matplotlib <https://matplotlib.org/>`_."""

import matplotlib.pyplot as plt
import re
import os

from config_handling import get_cfg

cfg = get_cfg()


def construct_graph(x, y, title, fname, **kwargs):
    """Helper function to create a graph and save it.

    :param x: The points' x-coordinates.
    :type x: list
    :param y: The points' y-coordinates.
    :type y: list
    :param title: The title of the graph, either as a template string or not.
    :type title: str
    :param fname: The file name of the graph or a template string for it.
    :type fname: str
    :param kwargs: Translation dict for chained `replace <https://docs.python.org/3/library/stdtypes.html#str.replace>`_ calls.
    :type kwargs: str, optional
    """
    for to_translate, translation in kwargs.items():
        title = title.replace(to_translate, translation)
        fname = fname.replace(to_translate, translation)

    plt.ylim(0, cfg.ylims[kwargs['KEY']])
    plt.plot(x, y)
    plt.title(title)
    plt.savefig(fname + '.png')
    plt.close()


def main():
    """Get data from all of the runs and make a graph for each variable's average."""

    graphs = {}
    vals = [file for file in os.listdir('.') if 'val' in file]

    for val in vals:
        with open(val, 'r') as f:
            data = f.read()
            all_x = re.findall('\d+(?=:)', data)
            all_k = re.findall('[a-z]+', data[0:data.find('\n')])
            all_v = re.findall('\d+(?=\|)', data)
            if not not graphs:
                for k in all_k:
                    translated = cfg.var_translation[k]
                    graphs[translated] = {}

        for k_place, k in enumerate(all_k):
            k_vals = [v for val_place, v in enumerate(all_v) if val_place % len(all_k) == k_place]
            k = cfg.var_translation[k]
            run = val.replace('val', '').replace('.txt', '')
            graphs[k][run] = [(x, y) for x, y in zip(all_x, k_vals)]

    for k, v in graphs.items():
        avgs_x = []
        avgs_y = []
        for n in range(min([len(v[run]) for run in v])):
            x_points = [int(v[run][n][0]) for run in v]
            y_points = [int(v[run][n][1]) for run in v]
            avgs_x.append(sum(x_points) // len(x_points))
            avgs_y.append(sum(y_points) // len(y_points))

        construct_graph(avgs_x,
                        avgs_y,
                        cfg.title_format,
                        cfg.fname_format,
                        KEY=k)


if __name__ == '__main__':
    main()
