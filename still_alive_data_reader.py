import struct
from typing import Iterator


def read_lines() -> Iterator[tuple[float, str]]:
    with open('still_alive.dat', 'rb') as fp:
        while time_b := fp.read(8):
            time: float = struct.unpack('>d', time_b)[0]
            line = fp.read(struct.unpack('>H', fp.read(2))[0]).decode()
            yield time, line


def read_chars() -> Iterator[tuple[float, str]]:
    for (time, line) in read_lines():
        if not line:
            yield time, ''
            continue
        delay = time / len(line)
        for c in line:
            yield delay, c
