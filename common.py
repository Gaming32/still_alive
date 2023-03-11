import os
import sys


if len(sys.argv) == 1:
    print(f'Usage: {sys.argv[0]} <still_alive|want_you_gone> [path_to_steamapps_common]')
    sys.exit(1)

portal_2 = sys.argv[1] == 'want_you_gone'

if len(sys.argv) > 2:
    steam_common = sys.argv[2]
else:
    for steam_dir in [
        'C:\\Program Files (x86)\\Steam',
        'C:\\Program Files\\Steam',
        os.path.expanduser('~/.local/share/Steam'),
        os.path.expanduser('~/.var/app/com.valvesoftware.Steam/data/Steam'),
        os.path.expanduser('~/Library/Application Support/Steam'),
    ]:
        if os.path.isdir(steam_dir):
            steam_common = f'{steam_dir}/steamapps/common'
            break
    else:
        print("The location of Steam couldn't be determined automatically. Please specify the location manually.")
        sys.exit(1)

portal_root = f'{steam_common}/Portal{" 2" * portal_2}/portal{"2" * portal_2}'
vpk_path = f'{portal_root}/{"pak01" if portal_2 else "portal_pak"}_dir.vpk'
