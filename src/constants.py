SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CHIP_8_TIMER_CLOCK = 60
CHIP_8_CPU_CLOCK = 540
CHIP_8_MEMORY_SIZE = 4096
CHIP_8_ROM_START = 0x200
CHIP_8_FONTSET = (
    (0xF0, 0x90, 0x90, 0x90, 0xF0),  # 0
    (0x20, 0x60, 0x20, 0x20, 0x70),  # 1
    (0xF0, 0x10, 0xF0, 0x80, 0xF0),  # 2
    (0xF0, 0x10, 0xF0, 0x10, 0xF0),  # 3
    (0x90, 0x90, 0xF0, 0x10, 0x10),  # 4
    (0xF0, 0x80, 0xF0, 0x10, 0xF0),  # 5
    (0xF0, 0x80, 0xF0, 0x90, 0xF0),  # 6
    (0xF0, 0x10, 0x20, 0x40, 0x40),  # 7
    (0xF0, 0x90, 0xF0, 0x90, 0xF0),  # 8
    (0xF0, 0x90, 0xF0, 0x10, 0xF0),  # 9
    (0xF0, 0x90, 0xF0, 0x90, 0x90),  # A
    (0xE0, 0x90, 0xE0, 0x90, 0xE0),  # B
    (0xF0, 0x80, 0x80, 0x80, 0xF0),  # C
    (0xE0, 0x90, 0x90, 0x90, 0xE0),  # D
    (0xF0, 0x80, 0xF0, 0x80, 0xF0),  # E
    (0xF0, 0x80, 0xF0, 0x80, 0x80),  # F
)
CHIP_8_DEBUG_MODE = False
