@echo off
python -m pip install -Ur requirements.txt
if errorlevel 1 (
    cls
    echo You need Python installed to run this.
    pause
    exit /b
)
python extract_files.py %1
if errorlevel 1 (
    cls
    echo You need to have %GAME_NAME% installed to run this.
    pause
    exit /b
)
python generate_data.py %1
python still_alive.py %1
