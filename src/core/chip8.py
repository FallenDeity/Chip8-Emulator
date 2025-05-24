import array
import pathlib
import random
import typing as t
import winsound

from src.core.keyboard import Keyboard
from src.core.memory import Memory
from src.core.registers import Registers

if t.TYPE_CHECKING:
    from src.gui.screen import Display


class Chip8:
    wait_for_key: int | None = None

    def __init__(self, rom_path: str | pathlib.Path) -> None:
        self.registers = Registers()
        self.memory = Memory()
        self.stack = array.array("H", [0] * 16)
        self.keyboard = Keyboard()
        self.rom_path = rom_path
        self.opcode_map: dict[int, t.Callable[[int, "Display"], None]] = {
            0x0000: self.__opcode_0,
            0x1000: self.__opcode_1,
            0x2000: self.__opcode_2,
            0x3000: self.__opcode_3,
            0x4000: self.__opcode_4,
            0x5000: self.__opcode_5,
            0x6000: self.__opcode_6,
            0x7000: self.__opcode_7,
            0x8000: self.__opcode_8,
            0x9000: self.__opcode_9,
            0xA000: self.__opcode_A,
            0xB000: self.__opcode_B,
            0xC000: self.__opcode_C,
            0xD000: self.__opcode_D,
            0xE000: self.__opcode_E,
            0xF000: self.__opcode_F,
        }
        self.memory.load_rom(self.rom_path)

    def __opcode_0(self, opcode: int, display: "Display") -> None:
        tail = opcode & 0x00FF
        match tail:
            case 0xE0:
                display.clear_display()
            case 0xEE:
                self.registers.program_counter = self.stack.pop()
                self.registers.stack_pointer -= 1
            case _:
                raise ValueError(f"Unknown opcode: {opcode:04X}")

    def __opcode_1(self, opcode: int, _: "Display") -> None:
        nnn = opcode & 0x0FFF
        self.registers.program_counter = nnn

    def __opcode_2(self, opcode: int, _: "Display") -> None:
        nnn = opcode & 0x0FFF
        self.stack.append(self.registers.program_counter)
        self.registers.stack_pointer += 1
        self.registers.program_counter = nnn

    def __opcode_3(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        nn = opcode & 0x00FF
        if self.registers.V[f"V{x:X}"] == nn:
            self.registers.PC += 2

    def __opcode_4(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        nn = opcode & 0x00FF
        if self.registers.V[f"V{x:X}"] != nn:
            self.registers.PC += 2

    def __opcode_5(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        if self.registers.V[f"V{x:X}"] == self.registers.V[f"V{y:X}"]:
            self.registers.PC += 2

    def __opcode_6(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        nn = opcode & 0x00FF
        self.registers.V[f"V{x:X}"].value = nn

    def __opcode_7(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        nn = opcode & 0x00FF
        self.registers.V[f"V{x:X}"] += nn

    def __opcode_8(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        n = opcode & 0x000F
        match n:
            case 0x0:
                self.registers.V[f"V{x:X}"].value = int(self.registers.V[f"V{y:X}"])
            case 0x1:
                self.registers.V[f"V{x:X}"] |= int(self.registers.V[f"V{y:X}"])
            case 0x2:
                self.registers.V[f"V{x:X}"] &= int(self.registers.V[f"V{y:X}"])
            case 0x3:
                self.registers.V[f"V{x:X}"] ^= int(self.registers.V[f"V{y:X}"])
            case 0x4:
                result = int(self.registers.V[f"V{x:X}"]) + int(self.registers.V[f"V{y:X}"])
                self.registers.VF.value = result > 255
                self.registers.V[f"V{x:X}"].value = result % 256
            case 0x5:
                result = int(self.registers.V[f"V{x:X}"]) - int(self.registers.V[f"V{y:X}"])
                self.registers.VF.value = result >= 0
                self.registers.V[f"V{x:X}"].value = result % 256
            case 0x6:
                self.registers.VF.value = int(self.registers.V[f"V{x:X}"]) & 1
                self.registers.V[f"V{x:X}"] >>= 1
            case 0x7:
                result = int(self.registers.V[f"V{y:X}"]) - int(self.registers.V[f"V{x:X}"])
                self.registers.VF.value = result >= 0
                self.registers.V[f"V{x:X}"].value = result % 256
            case 0xE:
                self.registers.VF.value = (int(self.registers.V[f"V{x:X}"]) >> 7) & 1
                self.registers.V[f"V{x:X}"] <<= 1
            case _:
                raise ValueError(f"Unknown opcode: {opcode:04X}")

    def __opcode_9(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        if self.registers.V[f"V{x:X}"] != self.registers.V[f"V{y:X}"]:
            self.registers.PC += 2

    def __opcode_A(self, opcode: int, _: "Display") -> None:
        nnn = opcode & 0x0FFF
        self.registers.I.value = nnn

    def __opcode_B(self, opcode: int, _: "Display") -> None:
        nnn = opcode & 0x0FFF
        self.registers.program_counter = nnn + int(self.registers.V["V0"])

    def __opcode_C(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        nn = opcode & 0x00FF
        random_value = random.randint(0, 255)
        self.registers.V[f"V{x:X}"].value = random_value & nn

    def __opcode_D(self, opcode: int, display: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        n = opcode & 0x000F
        self.registers.VF.value = 0
        for i in range(n):
            sprite = int(self.memory[int(self.registers.I) + i])
            for j in range(8):
                if (sprite >> (7 - j)) & 1:
                    x_pos = int(self.registers.V[f"V{x:X}"]) + j
                    y_pos = int(self.registers.V[f"V{y:X}"]) + i
                    if x_pos >= display.width or y_pos >= display.height:
                        continue
                    if display.get_pixel(x_pos, y_pos):
                        self.registers.VF.value = 1
                    display.set_pixel(x_pos, y_pos, not display.get_pixel(x_pos, y_pos))

    def __opcode_E(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        tail = opcode & 0x00FF
        match tail:
            case 0x9E:
                if self.keyboard.is_key_pressed(int(self.registers.V[f"V{x:X}"])):
                    self.registers.PC += 2
            case 0xA1:
                if not self.keyboard.is_key_pressed(int(self.registers.V[f"V{x:X}"])):
                    self.registers.PC += 2
            case _:
                raise ValueError(f"Unknown opcode: {opcode:04X}")

    def __opcode_F(self, opcode: int, _: "Display") -> None:
        x = (opcode >> 8) & 0x0F
        tail = opcode & 0x00FF
        match tail:
            case 0x07:
                self.registers.V[f"V{x:X}"].value = int(self.registers.DT)
            case 0x0A:
                self.wait_for_key = x
            case 0x15:
                self.registers.DT.value = int(self.registers.V[f"V{x:X}"])
            case 0x18:
                self.registers.ST.value = int(self.registers.V[f"V{x:X}"])
            case 0x1E:
                result = int(self.registers.I) + int(self.registers.V[f"V{x:X}"])
                self.registers.VF.value = result > 0xFFF
                self.registers.I.value = result % 0x1000
            case 0x29:
                self.registers.I.value = int(self.registers.V[f"V{x:X}"]) * 5
            case 0x33:
                value = int(self.registers.V[f"V{x:X}"])
                self.memory[int(self.registers.I)] = value // 100
                self.memory[int(self.registers.I) + 1] = (value // 10) % 10
                self.memory[int(self.registers.I) + 2] = value % 10
            case 0x55:
                for i in range(x + 1):
                    self.memory[int(self.registers.I) + i] = int(self.registers.V[f"V{i:X}"])
                self.registers.I += x + 1
            case 0x65:
                for i in range(x + 1):
                    self.registers.V[f"V{i:X}"].value = int(self.memory[int(self.registers.I) + i])
                self.registers.I += x + 1
            case _:
                raise ValueError(f"Unknown opcode: {opcode:04X}")

    def timers_60Hz(self) -> None:
        if int(self.registers.DT) > 0:
            self.registers.DT -= 1
        if int(self.registers.ST) > 0:
            self.registers.ST -= 1
            beep_duration_ms = int((1 / 60) * 1000)
            winsound.Beep(440, beep_duration_ms)

    def cycle(self, display: "Display") -> None:
        if self.wait_for_key is not None:
            if any(self.keyboard.is_key_pressed(i) for i in range(16)):
                key = next((i for i in range(16) if self.keyboard.is_key_pressed(i)), None)
                assert key is not None, "Key not found"
                self.registers.V[f"V{self.wait_for_key:X}"].value = key
                self.wait_for_key = None
            return
        opcode = self.fetch_opcode()
        self.execute_opcode(opcode, display)

    def execute_opcode(self, opcode: int, display: "Display") -> None:
        opcode_type = opcode & 0xF000
        if opcode_type in self.opcode_map:
            self.opcode_map[opcode_type](opcode, display)
        else:
            raise ValueError(f"Unknown opcode: {opcode:04X}")

    def fetch_opcode(self) -> int:
        pc = self.registers.program_counter
        opcode = int(self.memory[pc]) << 8 | int(self.memory[pc + 1])
        self.registers.PC += 2
        return opcode

    def reset(self) -> None:
        self.registers = Registers()
        self.memory = Memory()
        self.stack = array.array("H", [0] * 16)
        self.keyboard = Keyboard()
        self.wait_for_key = None
        self.memory.load_rom(self.rom_path)
