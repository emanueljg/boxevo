boxevo
======

2D-simulated evolution in Python using PyGame.

![Boxevo](https://media.giphy.com/media/cjcK4Ux5AZkw11UTNR/giphy.gif)

Installation (Windows)
----------------------

#### Cloning the repo

``` {.bash}
git clone https://github.com/NihilistBrew/boxevo.git
```

#### Downloading the repo

Link to .zip: https://github.com/NihilistBrew/boxevo/archive/master.zip

#### Using get\_simulation.bat

**This will wipe an already existing `simulation` directory!**

-   Create a `.txt` file and paste the following into it:

``` {.bash}
REM from tools\get_simulation.bat

@echo off

rd /s /q simulation

curl -L -O https://codeload.github.com/NihilistBrew/boxevo/zip/master
tar xf master

xcopy boxevo-master\simulation simulation /i /s
rd /s /q boxevo-master
del master
```

-   `Save as...`
-   It can be named whatever, but it must have `.bat` in the end.
    Example: `download.bat`.
-   Run the `.bat` file.

The `simulation` directoy will be created in the same directory that he
`.bat` file is in.

The temporary files (`master`, `boxevo-master`) will be deleted when the
process is done, subsequently closing the command prompt.

#### Using build\_simulation.bat

**This will wipe an already existing `simulation` directory!**

If you want to, you can compile the `simulation` directory and its
content straight from source. A new `simulation` directory will be
created.

After having cloned or downloaded the repository, run
`build_simulation`.

Usage
-----

#### Tweaking

The installation process will either result in either the whole
repository directory or just `simulation`. This does not matter, since
that directory is the only thing you need for running the program.

Where ever the directory may exists, open it. There are a few optional
things you can tweak before running the simulation:

-   Open `simulation\bundle\config.py` with any text editor. The
    variables here will all modify the simulation to one degree or
    another. After making a change, press `ctrl+s` to save it.
    -   Tip: For convenience of future simulations, you can keep it open
        and changing/saving it multiple times without having to re-open
        it.
-   To change the images of the sprites:
    -   Copy and paste an image of either an entity or a food sprite, or
        an image to be used as both.
    -   Change the relevant config variables (`cfg.entity_image` and/or
        `food_image`) to match the file name of the new images.
    -   Done!

#### Running

After you're finished tweaking and want to try it out, you have two
options:

1.  Run `simulation\bundle\startworld.exe`.

    -   This will create a single world populated by sprites that run
        for as long as the program is opened.
    -   The run will create a single text file with evolutionary data,
        named `val.txt`.
    -   Beyond the `val.txt`, no statistics/graphing will be generated.

2.  Run `simulation\simulate.exe`.

    -   This will run `startworld.exe` for as many times (`cfg.runs`)
        and as long (`cfg.duration`) as specified in the config.
    -   Each execution creates a dated directory which contains all of
        the runs spawned by one execution of `simulate.exe`.
    -   Each run will generate a text file with evolutionary data, named
        `val(run).txt`.
    -   These `val.txt` files are in turn read by a graphing tool, which
        generates several things.
        -   Each run gets a graph of the averages of the different
            evolutionary traits. This graph is by default
            (`cfg.run_fname_format`) saved as `RUN, KEY.png`, where
            `RUN = run number` and `KEY = evolutionary trait`.
        -   Each evolutionary trait also gets a graph describing its
            average progression across all runs, in essence being *"an
            average of an average"*. This graph is by default
            (`cfg.avg_fname_format`) saved as `KEY, medelvärde.png`.
        -   If `cfg.avg_tables == True`, text files corresponding to the
            "average of the average" graphs are created, containing all
            of the data points. These files are saved by default
            (`cfg.avg_table_fname`) as `KEY, text.txt`.
        -   Additionally, if `cfg.enable_spreadsheet == True`, a
            spreadsheet is created from the values of all traits
            selected in `cfg.spreadsheet_vars`, fetched from `.txt`
            files in `cfg.to_queue`. `val` files and *"average of
            average"* files are supported.

Documentation
-------------

Docs are hosted at https://boxevo.readthedocs.io.

License
-------

This project is licensed under the GNU General Public License v3.0 - see
`LICENSE.md` for details. 