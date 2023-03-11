import sys

from vpk_reader import VpkFile

OUTRO_FIND = '"OutroSongLyrics"\n{\n\n'

portal_root = (
    sys.argv[1]
    if len(sys.argv) > 1
    else 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal\\portal'
)

print('Reading dir.vpk')
credits_txt = (
    VpkFile(f'{portal_root}/portal_pak_dir.vpk')
        .get_bytes('scripts/credits.txt')
        .decode()
        .replace('\r\n', '\n')
)

outro_index = credits_txt.index(OUTRO_FIND)
outro_end = credits_txt.index('\n\t\t\n}')

print('Extracting OutroSongLyrics from credits.txt')
with open('OutroSongLyrics.txt', 'w') as fp:
    fp.write(credits_txt[outro_index + len(OUTRO_FIND):outro_end])


print('Extracting portal_lyrics from portal_english.txt')
with open(f'{portal_root}/resource/portal_english.txt', encoding='utf-16') as fp:
    english_txt = fp.read()

with open('portal_lyrics.txt', 'w') as fp:
    fp.write(english_txt[english_txt.index('"portal_lyrics_01"'):-len('\n} \n}\n')])
