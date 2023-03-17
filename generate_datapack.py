import json
import os
import shutil
import subprocess

import tqdm
import vpk

import still_alive_data_reader
from common import portal_2, vpk_path

LINE_COUNT = 20 if portal_2 else 23

print('Extracting song')
song_name = 'portal2_want_you_gone.wav' if portal_2 else 'portal_still_alive.mp3'
with vpk.open(vpk_path) as vf:
    with vf[f'sound/music/{song_name}'] as fp_in:
        fp_in.save(song_name)


target_time = 0
current_time = 0
frames: list[tuple[str, int]] = []
current_frame = ''

print('Preparing frames')
for (delay, char) in still_alive_data_reader.read_chars():
    if char == '\0':
        current_frame = ''
    else:
        current_frame += char
    target_time += delay
    time_diff = target_time - current_time
    ticks = round(time_diff * 20)
    current_time += ticks / 20
    if ticks > 0:
        frames.append((current_frame, ticks))


base_name = 'want_you_gone' if portal_2 else 'still_alive'
base_dir = f'minecraft/{base_name}'
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(base_dir)

print('Converting audio')
resources_dir = f'{base_dir}_resources'
if os.path.exists(resources_dir):
    shutil.rmtree(resources_dir)
os.makedirs(resources_dir)
with open(f'{resources_dir}/pack.mcmeta', 'w') as fp:
    json.dump({
        'pack': {
            'pack_format': 9,
            'description': 'Resources for music'
        }
    }, fp)
assets_dir = f'{resources_dir}/assets/{base_name}'
os.makedirs(f'{assets_dir}/sounds')
pipe = subprocess.Popen(
    ['ffmpeg', '-i', song_name, f'{assets_dir}/sounds/{base_name}.ogg'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
with open(f'{assets_dir}/sounds.json', 'w') as fp:
    json.dump({
        base_name: {
            'sounds': [
                {
                    'name': f'{base_name}:{base_name}',
                    'stream': True
                }
            ]
        }
    }, fp)


print('Building frames')
with open(f'{base_dir}/pack.mcmeta', 'w') as fp:
    json.dump({
        'pack': {
            'description': 'Datapack for music',
            'pack_format': 10
        }
    }, fp)
functions_dir = f'{base_dir}/data/{base_name}/functions'
if os.path.exists(functions_dir):
    shutil.rmtree(functions_dir)
os.makedirs(functions_dir)

frame_prefix = f'{functions_dir}/frames'
os.mkdir(frame_prefix)
frame_prefix += '/frame'
played_sound = False
for (i, (frame, delay)) in enumerate(tqdm.tqdm(frames, unit='frame')):
    line_count = frame.count('\n') + 1
    with open(f'{frame_prefix}_{i}.mcfunction', 'w') as fp:
        if not played_sound and len(frame) > 2:
            if portal_2 and frame[-1] == '2':
                print(frame)
                played_sound = True
            elif not portal_2 and frames[i - 1][1] > 50:
                played_sound = True
            if played_sound:
                fp.write(f'execute as @a at @s run playsound {base_name}:{base_name} record @s\n')
        fp.write('tellraw @a ')
        json.dump(frame + '\n' * (LINE_COUNT - line_count), fp)
        fp.write('\n')
        if i < len(frames) - 1:
            fp.write(f'schedule function {base_name}:frames/frame_{i + 1} {delay}t\n')

with open(f'{functions_dir}/{base_name}.mcfunction', 'w') as fp:
    fp.write(f'function {base_name}:frames/frame_0\n')


print('Waiting for audio conversion to finish')
if err := pipe.wait():
    print('ffmpeg exited with code', err)
