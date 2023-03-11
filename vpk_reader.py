"""
This code is based on https://developer.valvesoftware.com/wiki/VPK_File_Format/vpk2_reader.py
"""

import struct
from typing import BinaryIO


class VpkEntry:
    path: str
    crc: int
    archive_index: int
    offset: int
    length: int
    preload: bytes


class VpkFile:
    base_path: str
    signature: bytes
    version: int
    directory_len: int
    unknown: tuple[int, int, int, int]
    entries: dict[str, VpkEntry]

    def __init__(self, base_path: str) -> None:
        self.base_path = base_path.removesuffix('_dir.vpk')
        self._populate_entries()

    def _populate_entries(self) -> None:
        with open(f'{self.base_path}_dir.vpk', 'rb') as fp:
            self.signature = fp.read(4)
            self.version = get_int4(fp)
            self.directory_len = get_int4(fp)
            self.unknown = (get_int4(fp), get_int4(fp), get_int4(fp), get_int4(fp))
            self.entries = {}
            while extension := get_sz(fp):
                while folder := get_sz(fp):
                    while filename := get_sz(fp):
                        cur_entry = VpkEntry()
                        cur_entry.path = f'{folder}/{filename}.{extension}'
                        cur_entry.crc = get_int4(fp)
                        preload_bytes = get_int2(fp)
                        cur_entry.archive_index = get_int2(fp)
                        cur_entry.offset = get_int4(fp)
                        cur_entry.length = get_int4(fp)
                        get_int2(fp) # Terminator
                        cur_entry.preload = fp.read(preload_bytes)
                        self.entries[cur_entry.path] = cur_entry

    def get_bytes(self, file: str | VpkEntry) -> bytes:
        if isinstance(file, str):
            file = self.entries[file]
        result = file.preload
        if file.length:
            with open(f'{self.base_path}_{file.archive_index:03}.vpk', 'rb') as fp:
                fp.seek(file.offset)
                result += fp.read(file.length)
        return result


def get_int4(fp: BinaryIO) -> int:
    return int(struct.unpack('I', fp.read(4))[0])


def get_int2(fp: BinaryIO) -> int:
    return int(struct.unpack('H', fp.read(2))[0])


def get_sz(fp: BinaryIO) -> str:
    result = ''
    while (cur := fp.read(1)) != b'\0':
        result += struct.unpack('c', cur)[0].decode('ascii')
    return result
