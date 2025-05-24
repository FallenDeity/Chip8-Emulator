import typing as t

import attrs

if t.TYPE_CHECKING:
    type ValueT = attrs.Attribute[int]
else:
    type ValueT = attrs.Attribute


def _register_validator(instance: "Register", attribute: ValueT, value: t.Any) -> None:
    if not (0 <= value < 2**instance.size):
        raise ValueError(f"Register {attribute.name} must be between 0 and {2 ** instance.size - 1}.")


def _size_validator(instance: "Register", attribute: ValueT, value: t.Any) -> None:
    if value not in (8, 16):
        raise ValueError(f"Register {attribute.name} must be either 8 or 16 bits.")


@attrs.define(slots=True, kw_only=True, eq=False)
class Register:
    name: str
    value: int = attrs.field(default=0, validator=[attrs.validators.instance_of(int), _register_validator])
    size: int = attrs.field(default=8, validator=[attrs.validators.instance_of(int), _size_validator])

    def __repr__(self) -> str:
        return f"<{self.name}: 0x{self.value:0{self.size // 4}X} ({self.value})>"

    def __int__(self) -> int:
        return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Register):
            return self.value == other.value and self.size == other.size and self.name == other.name
        if isinstance(other, int):
            return self.value == other
        return False

    def __add__(self, other: int) -> "Register":
        if isinstance(other, Register):
            return Register(name=self.name, value=(self.value + other.value) % (2**self.size), size=self.size)
        return Register(name=self.name, value=(self.value + other) % (2**self.size), size=self.size)

    def __sub__(self, other: int) -> "Register":
        if isinstance(other, Register):
            return Register(name=self.name, value=(self.value - other.value) % (2**self.size), size=self.size)
        return Register(name=self.name, value=(self.value - other) % (2**self.size), size=self.size)

    def __lshift__(self, other: int) -> "Register":
        return Register(name=self.name, value=(self.value << other) % (2**self.size), size=self.size)

    def __rshift__(self, other: int) -> "Register":
        return Register(name=self.name, value=(self.value >> other) % (2**self.size), size=self.size)

    def __and__(self, other: int) -> "Register":
        if isinstance(other, Register):
            return Register(name=self.name, value=(self.value & other.value) % (2**self.size), size=self.size)
        return Register(name=self.name, value=(self.value & other) % (2**self.size), size=self.size)

    def __or__(self, other: int) -> "Register":
        if isinstance(other, Register):
            return Register(name=self.name, value=(self.value | other.value) % (2**self.size), size=self.size)
        return Register(name=self.name, value=(self.value | other) % (2**self.size), size=self.size)

    def __xor__(self, other: int) -> "Register":
        if isinstance(other, Register):
            return Register(name=self.name, value=(self.value ^ other.value) % (2**self.size), size=self.size)
        return Register(name=self.name, value=(self.value ^ other) % (2**self.size), size=self.size)


@attrs.define(slots=True, kw_only=True)
class Registers:
    V: dict[str, Register] = attrs.field(factory=lambda: {f"V{i:X}": Register(name=f"V{i:X}") for i in range(16)})
    I: Register = Register(name="I", size=16)  # noqa: E741
    DT: Register = Register(name="DT", size=8)
    ST: Register = Register(name="ST", size=8)

    PC: Register = Register(name="PC", size=16, value=0x200)
    SP: Register = Register(name="SP", size=8)

    def __getattr__(self, name: str) -> Register:
        if name in self.V:
            return self.V[name]
        raise AttributeError(f"Register '{name}' not found.")

    @property
    def stack_pointer(self) -> int:
        return int(self.SP)

    @stack_pointer.setter
    def stack_pointer(self, value: int) -> None:
        self.SP.value = value

    @property
    def program_counter(self) -> int:
        return int(self.PC)

    @program_counter.setter
    def program_counter(self, value: int) -> None:
        self.PC.value = value
