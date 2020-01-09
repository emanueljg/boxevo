
Installation (Windows)
----------------------

#### Cloning the repo

``` {.bash}
git clone https://github.com/NihilistBrew/boxevo.git
```

#### Downloading the repo

Link to .zip: https://github.com/NihilistBrew/boxevo/archive/master.zip

#### Using get\_simulation.bat

**This will wipe an already existing ``simulation`` directory!**

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

**This will wipe an already existing ``simulation`` directory!**

If you want to, you can compile the `simulation` directory and its
content straight from source. A new `simulation` directory will be
created.

After having cloned or downloaded the repository, run
`build_simulation`.
