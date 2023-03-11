import os
import sys
import time

import still_alive_data_reader
from vpk_reader import VpkFile

portal_root = (
    sys.argv[1]
    if len(sys.argv) > 1
    else 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal\\portal'
)
with open('still_alive.mp3', 'wb') as fp:
    fp.write(VpkFile(f'{portal_root}/portal_pak_dir.vpk').get_bytes('sound/music/portal_still_alive.mp3'))


played_sound = False

def start_playsound() -> None:
    try:
        import playsound
    except ModuleNotFoundError:
        pass
    else:
        try:
            playsound.playsound('still_alive.mp3', block=False)
        except playsound.PlaysoundException:
            print('playsound failed. Try installing playsound==1.2.2 as per https://stackoverflow.com/a/69547923/8840278.')
            sys.exit(1)


target_time = time.perf_counter()
clear_command = 'cls' if sys.platform == 'win32' else 'clear'
os.system(clear_command)
for (delay, char) in still_alive_data_reader.read_chars():
    if char == '\0':
        os.system(clear_command)
    else:
        sys.stdout.write(char)
        sys.stdout.flush()
    target_time += delay
    while time.perf_counter() < target_time:
        pass
    if delay > 2.5 and not played_sound:
        played_sound = True
        start_playsound()

print()
