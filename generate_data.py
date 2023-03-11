import struct
from typing import Optional

from common import portal_2

translations: Optional[dict[str, str]]
if not portal_2:
    print('Reading portal_lyrics.txt')
    translations = {}
    with open('portal_lyrics.txt') as fp:
        for line in fp:
            parts = line.strip().split(' \t', 1)
            translations[parts[0][1:-1]] = parts[1][1:-1]
else:
    translations = None


print('Reading OutroSongLyrics.txt and writing still_alive.dat')
with open('still_alive.dat', 'wb') as fp_out:
    with open('OutroSongLyrics.txt') as fp_in:
        for line in fp_in:
            line = line.strip()[1:-len('" "CreditsOutroText"')]
            rbracket_index = line.index(']')
            time = float(line[1:rbracket_index])
            line = line[rbracket_index + 1:]
            if line.startswith('<<<'): # I don't know what these do
                line = line[line.index('>>>') + 3:]
            newline = '\n'
            if line.isspace():
                line = ''
                newline = ''
            else:
                if line[0] == '*':
                    line = line[1:]
                    newline = ''
                if line[0] == '#' and translations is not None:
                    line = translations[line[1:]]
                elif line == '^':
                    line = '\n'
                    newline = ''
                elif line == '&':
                    line = '\0'
                    newline = ''
            line_b = (line + newline).encode()
            fp_out.write(struct.pack('>d', time))
            fp_out.write(struct.pack('>H', len(line_b)))
            fp_out.write(line_b)
