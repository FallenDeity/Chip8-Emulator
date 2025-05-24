import pathlib

from src.constants import (
    CHIP_8_FONTSET,
    CHIP_8_MEMORY_SIZE,
    CHIP_8_ROM_START,
)


class Memory:
    def __init__(self, size: int = CHIP_8_MEMORY_SIZE) -> None:
        self.size = size
        self.memory = bytearray(size)
        self._load_fontset()

    def _load_fontset(self) -> None:
        for i, font in enumerate(CHIP_8_FONTSET):
            self.memory[i * 5 : (i + 1) * 5] = bytearray(font)

    def load_rom(self, rom_path: str | pathlib.Path) -> None:
        with open(rom_path, "rb") as rom_file:
            rom_data = rom_file.read()
            if len(rom_data) + CHIP_8_ROM_START > self.size:
                raise ValueError("ROM size exceeds memory limit.")
            self.memory[CHIP_8_ROM_START : CHIP_8_ROM_START + len(rom_data)] = rom_data

    def __getitem__(self, index: int | slice) -> int | bytearray:
        if isinstance(index, slice):
            return self.memory[index]
        return self.memory[index]

    def __setitem__(self, index: int | slice, value: int | bytes | bytearray) -> None:
        if isinstance(index, slice):
            if not isinstance(value, (bytes, bytearray)):
                raise TypeError("Slice assignment requires a bytes or bytearray value.")
            self.memory[index] = value
        else:
            if not isinstance(value, int):
                raise TypeError("Memory value must be an integer.")
            if not (0 <= value <= 0xFF):
                raise ValueError("Memory value must be between 0 and 255.")
            self.memory[index] = value
