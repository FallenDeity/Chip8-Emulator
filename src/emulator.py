import pathlib
import time

import pygame

from src.constants import CHIP_8_CPU_CLOCK, CHIP_8_DEBUG_MODE, CHIP_8_TIMER_CLOCK, SCREEN_HEIGHT, SCREEN_WIDTH
from src.core.chip8 import Chip8
from src.gui.screen import Display


class Window:
    keymap = {
        pygame.K_1: "KEY1",
        pygame.K_2: "KEY2",
        pygame.K_3: "KEY3",
        pygame.K_4: "KEYC",
        pygame.K_q: "KEY4",
        pygame.K_w: "KEY5",
        pygame.K_e: "KEY6",
        pygame.K_r: "KEYD",
        pygame.K_a: "KEY7",
        pygame.K_s: "KEY8",
        pygame.K_d: "KEY9",
        pygame.K_f: "KEYE",
        pygame.K_z: "KEYA",
        pygame.K_x: "KEY0",
        pygame.K_c: "KEYB",
        pygame.K_v: "KEYF",
    }

    def __init__(self, rom_path: str | pathlib.Path) -> None:
        pygame.init()
        pygame.font.init()

        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CHIP-8 Emulator")

        self.clock = pygame.time.Clock()
        self.chip = Chip8(rom_path)
        self.display = Display()
        self.last_timer_time = time.perf_counter()
        self.last_cycle_time = time.perf_counter()

    def run(self):
        running = True
        while running:
            now = time.perf_counter()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.on_keydown(event.key)
                if event.type == pygame.KEYUP:
                    self.on_keyup(event.key)

            if now - self.last_timer_time >= 1 / CHIP_8_TIMER_CLOCK:
                self.chip.timers_60Hz()
                self.last_timer_time = now

            if now - self.last_cycle_time >= 1 / CHIP_8_CPU_CLOCK:
                self.chip.cycle(self.display)
                self.last_cycle_time = now

            self.window.fill((0, 0, 0))

            surface = self.display.render()
            cx = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.window.blit(surface, cx.topleft)
            pygame.draw.rect(self.window, (255, 255, 255), cx, 2)

            if CHIP_8_DEBUG_MODE:
                status_text = f"PC: 0x{self.chip.registers.program_counter:X} SP: 0x{self.chip.registers.stack_pointer:X} DT: 0x{int(self.chip.registers.DT):X} ST: 0x{int(self.chip.registers.ST):X}"
                font = pygame.font.SysFont("Arial", 20)
                text_surface = font.render(status_text, False, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
                self.window.blit(text_surface, text_rect.topleft)

                for i in range(16):
                    register_value = f"V{i}: 0x{int(self.chip.registers.V[f'V{i:X}']):X}"
                    text_surface = font.render(register_value, False, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(10, 30 + i * 20))
                    self.window.blit(text_surface, text_rect.topleft)
                text_surface = font.render("Registers", False, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(10, 10))
                self.window.blit(text_surface, text_rect.topleft)

                for i in range(len(self.chip.stack)):
                    stack_value = f"0x{self.chip.stack[i]:X}"
                    text_surface = font.render(stack_value, False, (255, 255, 255))
                    text_rect = text_surface.get_rect(topleft=(SCREEN_WIDTH - 100, 30 + i * 20))
                    self.window.blit(text_surface, text_rect.topleft)
                text_surface = font.render("Stack", False, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(SCREEN_WIDTH - 100, 10))
                self.window.blit(text_surface, text_rect.topleft)

                rom_path_text = f"ROM: {pathlib.Path(self.chip.rom_path).name}"
                text_surface = font.render(rom_path_text, False, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 10))
                self.window.blit(text_surface, text_rect.topleft)

            pygame.display.flip()

        pygame.quit()

    def on_keydown(self, key_code: int):
        if key_code in self.keymap:
            key = self.keymap[key_code]
            self.chip.keyboard.keymap[key].pressed = True

    def on_keyup(self, key_code: int):
        if key_code in self.keymap:
            key = self.keymap[key_code]
            self.chip.keyboard.keymap[key].pressed = False
