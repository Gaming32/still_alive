#!/usr/bin/env python3
import os
import sys
import time

import playsound
import vpk

import still_alive_data_reader
from common import portal_2, vpk_path

song_name = "portal2_want_you_gone.wav" if portal_2 else "portal_still_alive.mp3"
with vpk.open(vpk_path) as vf:
    with vf[f'sound/music/{song_name}'] as fp_in:
        fp_in.save(song_name)

played_sound = False

target_time = time.perf_counter()
clear_command = 'cls' if sys.platform == 'win32' else 'clear'
os.system(clear_command)
for (delay, char) in still_alive_data_reader.read_chars():
    if portal_2 and char == '2' and not played_sound:
        played_sound = True
        playsound.playsound(song_name, block=False)
    if char == '\0':
        os.system(clear_command)
    else:
        sys.stdout.write(char)
        sys.stdout.flush()
    target_time += delay
    while time.perf_counter() < target_time:
        pass
    if not portal_2 and delay > 2.5 and not played_sound:
        played_sound = True
        playsound.playsound(song_name, block=False)

print()
if portal_2:
    time.sleep(10) # Portal 2's credits.txt ends before the song
