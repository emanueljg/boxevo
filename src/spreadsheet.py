"""This module creates a spreadsheet of simulation stats.

Can run from :mod:`graph` if enabled in cofig (``cfg.enable_spreadsheet``), or run manually as a standalone executable.
"""

import xlsxwriter
import os
from copy import copy

from parsing import get_cfg, parse_val

cfg = get_cfg()


def data_time_trunc(x, y):
    """Shorten an array `y` with corresponding values of the time array `x` to only show values for whole minutes.

    :param x: The time array.
    :type x: list, tuple
    :param x: The target array.
    :type x: list, tuple
    :return: The truncated array as a list.
    :rtype: list
    """
    indexes = []
    minutes = 0
    for c, i in enumerate(x):
        if i / 60 > minutes:
            minutes += 1
            indexes.append(c)

    return [y[n] for n in indexes]


def main():
    """Run the program."""

    # Find files to be made into a spreadsheet and build queue -----------------------------------------

    texts = [file for file in os.listdir('.') if file.replace('.txt', '') in cfg.to_queue]
    queue = {}

    for text in texts:
        run = None
        data = {}
        with open(text, 'r') as f:
            if 'val' in text:
                run = text.replace('val', '').replace('.txt', '')
                data = parse_val(f.read())
            else:
                name = f'Medelvärde (av {cfg.runs} körningar)'
                queue.setdefault(name, {})
                all_x = []
                all_y = []
                for i in f.readlines():
                    x = i[:i.find(',')]
                    y = i.replace((x + ','), '').replace('\n', '')
                    all_x.append(int(x))
                    all_y.append(int(y))
                queue[name][text.replace('.txt', '')] = data_time_trunc(all_x, all_y)

        if 'val' in text:
            key_name = f'Körning {run}'
            queue[key_name] = {}
            for var in cfg.spreadsheet_vars:
                queue[key_name][var] = data_time_trunc(data['x'], data['k'][var])

    # Create spreadsheet file and setup everything -----------------------------------------

    wb = xlsxwriter.Workbook('spreadsheet.xlsx')
    ws = wb.add_worksheet()

    title_format = wb.add_format({**cfg.spreadsheet_format, 'border': 1})
    double_title_format = wb.add_format({**cfg.spreadsheet_format, 'border': 5})
    left_title_format = wb.add_format({**cfg.spreadsheet_format, 'left': 5, 'right': 1, 'bottom': 1})
    right_title_format = wb.add_format({**cfg.spreadsheet_format, 'right': 5, 'left': 1, 'bottom': 1})

    left_format = wb.add_format({'left': 5, 'valign': 'center'})
    right_format = wb.add_format({'right': 5, 'valign': 'center'})

    bottom_format = wb.add_format({'top': 5})

    ws.merge_range(0, 0, 1, 0, cfg.spreadsheet_x_column, double_title_format)
    ws.write_column(2, 0, range(cfg.duration // 60), right_format)

    # Write everything to spreadsheet ------------------------------------------------------------------------

    col_pointer = 1
    for item in queue:
        vars = queue[item]

        # Main title
        ws.merge_range(0, col_pointer, 0, col_pointer + len(vars) - 1, item, double_title_format)

        # Readjust the space of the average-value-column
        ws.set_column(col_pointer, col_pointer + len(vars) - 1, 15)

        # Write all variables for an item ---------------
        inner_col_pointer = col_pointer
        for c, (var, values) in enumerate(vars.items()):

            # Add border to the left (at the beginning)
            if c == 0:
                title = left_title_format
                normal = left_format
            # Add border to the right (at the end)
            elif c + 1 == len(vars):
                title = right_title_format
                normal = right_format
            # Normal behaviour (no borders)
            else:
                title = title_format
                normal = None

            # Write sub-title (variable names)
            ws.write(1, inner_col_pointer, var, title)
            # Write all values for a variable
            ws.write_column(2, inner_col_pointer, values, normal)

            inner_col_pointer += 1
        col_pointer += len(vars)

    # Write bottom border
    ws.write_row(cfg.duration // 60 + 2, 0, [None for _ in range(col_pointer)], bottom_format)

    # Close (and save) the spreadsheet
    wb.close()


if __name__ == '__main__':
    main()
