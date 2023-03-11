import sys


if len(sys.argv) == 1:
    print(f'Usage: {sys.argv[0]} <still_alive|want_you_gone> [path_to_steamapps_common]')
    sys.exit(1)

portal_2 = sys.argv[1] == 'want_you_gone'

steam_root = (
    sys.argv[2]
    if len(sys.argv) > 2
    else 'C:\\Program Files (x86)\\Steam\\steamapps\\common'
)
portal_root = f'{steam_root}/Portal{" 2" * portal_2}/portal{"2" * portal_2}'
vpk_path = f'{portal_root}/{"pak01" if portal_2 else "portal_pak"}_dir.vpk'
