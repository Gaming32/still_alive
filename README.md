# Still Alive

Play Still Alive and Want You Gone right in your console :)

## To run

### The easy way

Install Python 3.10 or later from [python.org](https://python.org), then double-click on `still_alive.bat` or `want_you_gone.bat`. `still_alive.bat` requires Portal to be installed, and `want_you_gone.bat` requires Portal 2 to be installed.

### The hard way

First run `extract_files.py` to extract the files from the game, then run `generate_data.py` to generate a `still_alive.dat`. `still_alive.dat` can be read with the `still_alive_data_reader` module.

If `extract_files.py` runs into a file not found error, then provide it with the path to your Portal installation's `portal` folder as an argument.
