@echo off
SETLOCAL EnableDelayedExpansion

for %%I in (.) do set base=%%~nxI
if not "!base!"=="tools" (cd tools)

(
echo .. This file was generated by tools\make_config_doc.bat
echo .. !date! !time:~0,8!
echo.
echo config
echo ======
echo .. automodule:: config
)>"new_config.rst"

for /F "tokens=*" %%A in (..\src\config.py) do (
    set line=%%A
    if not "!line:~0,2!" == "#:" (
        if not "!line!" == "" (
            if "!line:~0,2!" == "##" (
                set title=!line:#=!
                (
                echo.
                echo !title!
                echo ----------------
                )>>"new_config.rst"
            ) else (
                for /f "tokens=1 delims= " %%B in ("!line!") do (
                    set key=%%B
                )
                if not "!key:~0,3!" == ^"^"^"^"^" (
                    echo .. autodata:: !key!>>"new_config.rst"
                )
            )
        )
    )
)

mv new_config.rst ..\docs\source\config.rst

ENDLOCAL