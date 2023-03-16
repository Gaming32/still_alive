#!/bin/sh
python3 -m pip install -Ur requirements.txt
if [ $? -ne 0 ]; then
    echo You need Python 3 installed to run this.
    exit 1
fi
python3 ./extract_files.py $1
if [ $? -ne 0 ]; then
    exit 1
fi
python3 ./generate_data.py $1
python3 ./still_alive.py $1
