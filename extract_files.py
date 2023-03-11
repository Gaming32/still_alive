import vpk

from common import portal_2, portal_root, vpk_path

OUTRO_FIND = '"OutroSongLyrics"\n{\n' + '\n' * (not portal_2)

print('Reading credits.txt')
if portal_2:
    with open(f'{portal_root}/scripts/credits.txt') as fp:
        credits_txt = fp.read()
else:
    with vpk.open(vpk_path) as vfp:
        with vfp['scripts/credits.txt'] as fp:
            credits_txt = fp.read().decode().replace('\r\n', '\n')

outro_index = credits_txt.index(OUTRO_FIND)
outro_end = credits_txt.index('\n\t\t' * (not portal_2) + '\n}', outro_index)

print('Extracting OutroSongLyrics from credits.txt')
with open('OutroSongLyrics.txt', 'w') as fp:
    fp.write(credits_txt[outro_index + len(OUTRO_FIND):outro_end])


if not portal_2:
    print('Extracting portal_lyrics from portal_english.txt')
    with open(f'{portal_root}/resource/portal_english.txt', encoding='utf-16') as fp:
        english_txt = fp.read()

    with open('portal_lyrics.txt', 'w') as fp:
        fp.write(english_txt[english_txt.index('"portal_lyrics_01"'):-len('\n} \n}\n')])
