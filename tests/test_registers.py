import pytest

from core.registers import Register, Registers


@pytest.fixture
def register() -> Register:
    """Fixture for a default register."""
    return Register(name="V0", value=0, size=8)


@pytest.fixture
def registers() -> Registers:
    """Fixture for a default set of registers."""
    return Registers()


def test_registers_initialization(registers: Registers) -> None:
    """Test the initialization of registers."""
    assert len(registers.V) == 16
    assert registers.I.name == "I"
    assert registers.PC.name == "PC"
    assert registers.SP.name == "SP"
    assert registers.V5 == registers.V["V5"]


def test_register_repr(register: Register) -> None:
    """Test the string representation of a register."""
    assert repr(register) == "<V0: 0x00 (0)>"


def test_register_value(register: Register) -> None:
    """Test the value of a register."""
    assert register.value == 0
    register.value = 42
    assert register.value == 42
    with pytest.raises(ValueError):
        register.value = 256
    with pytest.raises(TypeError):
        register.value = "not an int"  # type: ignore[assignment]


def test_register_size(register: Register) -> None:
    """Test the size of a register."""
    assert register.size == 8
    register.size = 16
    assert register.size == 16
    with pytest.raises(ValueError):
        register.size = 32
    with pytest.raises(TypeError):
        register.size = "not an int"  # type: ignore[assignment]
