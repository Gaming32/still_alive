python -m pip install -Ur requirements.txt
python extract_files.py %1
python generate_data.py %1
python still_alive.py %1
