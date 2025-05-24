import pygame

CHIP_8_DISPLAY_WIDTH = 64
CHIP_8_DISPLAY_HEIGHT = 32
PIXEL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Display:
    def __init__(self):
        self.surface = pygame.Surface((CHIP_8_DISPLAY_WIDTH * PIXEL_SIZE, CHIP_8_DISPLAY_HEIGHT * PIXEL_SIZE))
        self.buffer = [[False] * CHIP_8_DISPLAY_WIDTH for _ in range(CHIP_8_DISPLAY_HEIGHT)]
        self.dirty: set[tuple[int, int]] = set()

    def set_pixel(self, x: int, y: int, value: bool) -> None:
        if 0 <= x < CHIP_8_DISPLAY_WIDTH and 0 <= y < CHIP_8_DISPLAY_HEIGHT:
            self.buffer[y][x] = value
            self.dirty.add((x, y))

    def get_pixel(self, x: int, y: int) -> bool:
        if 0 <= x < CHIP_8_DISPLAY_WIDTH and 0 <= y < CHIP_8_DISPLAY_HEIGHT:
            return self.buffer[y][x]
        return False

    def clear_display(self) -> None:
        for y in range(CHIP_8_DISPLAY_HEIGHT):
            for x in range(CHIP_8_DISPLAY_WIDTH):
                self.buffer[y][x] = False
        self.surface.fill(BLACK)
        self.dirty.clear()

    def render(self) -> pygame.Surface:
        for x, y in self.dirty:
            color = WHITE if self.buffer[y][x] else BLACK
            pygame.draw.rect(self.surface, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        self.dirty.clear()
        return self.surface

    @property
    def width(self) -> int:
        return CHIP_8_DISPLAY_WIDTH

    @property
    def height(self) -> int:
        return CHIP_8_DISPLAY_HEIGHT
