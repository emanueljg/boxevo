"""This module handles variable graphing using `matplotlib <https://matplotlib.org/>`_.

It also creates a child process, :mod:`spreadsheet`, if this is enabled in the :mod:`config` (``cfg.enable_spreadsheet``)
"""

import matplotlib.pyplot as plt
import re
import os
from win32process import CreateProcess, STARTUPINFO

from parsing import get_cfg, parse_val

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

    k = kwargs['KEY']

    if k in cfg.scaled_vars:
        y = [int(i // cfg.scaled_vars[k]) for i in y]

    plt.ylim(0, cfg.ylims[k])
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(cfg.axis_labels['x'])
    plt.ylabel(cfg.axis_labels[k])
    plt.savefig(fname + '.png')
    plt.close()


def main():
    """Get data from all of the runs and make a graph for each variable's average."""
    vals = [file for file in os.listdir('.') if 'val' in file]
    run_graphs = {}
    avg_graphs = {}
    for val in vals:
        with open(val, 'r') as f:
            run = val.replace('val', '').replace('.txt', '')
            data = parse_val(f.read())
            run_graphs[run] = data

    for run, graph in run_graphs.items():
        for k, v in graph['k'].items():
            construct_graph(x=graph['x'],
                            y=v,
                            title=cfg.run_title_format,
                            fname=cfg.run_fname_format,
                            RUN=run,
                            KEY=k)

            if len(v) < avg_graphs.setdefault(k, {}).setdefault('length', cfg.duration):
                avg_graphs[k]['length'] = len(v)
            avg_graphs[k].setdefault('x', []).append(graph['x'])
            avg_graphs[k].setdefault('y', []).append(v)

    for k, graph in avg_graphs.items():
        avgs_x = [sum(li) // len(li) for li in [[r[n] for r in graph['x']] for n in range(graph['length'])]]
        avgs_y = [sum(li) // len(li) for li in [[r[n] for r in graph['y']] for n in range(graph['length'])]]
        construct_graph(avgs_x,
                        avgs_y,
                        cfg.avg_title_format,
                        cfg.avg_fname_format,
                        KEY=k)

        if cfg.avg_tables:
            lines = '\n'.join([cfg.avg_table_data_format.replace('X', str(x)).replace('Y', str(y))
                               for x, y in zip(avgs_x, avgs_y)])
            with open(cfg.avg_table_fname_format.replace('KEY', k) + '.txt', 'w') as f:
                f.write(lines)

    if cfg.remove_non_statistics:
        os.system(f'del {cfg.entity_image} {cfg.food_image} {cfg.exe}')

    if cfg.enable_spreadsheet:
        CreateProcess(None, 'spreadsheet.exe', None, None, False, 0, None, None, STARTUPINFO())


if __name__ == '__main__':
    main()
