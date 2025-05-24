import typing as t

import attrs

if t.TYPE_CHECKING:
    type ValueT = attrs.Attribute[int]
else:
    type ValueT = attrs.Attribute


@attrs.define(slots=True, kw_only=True)
class Key:
    name: str
    value: int = attrs.field(
        default=0, validator=[attrs.validators.instance_of(int), attrs.validators.ge(0), attrs.validators.le(15)]
    )
    pressed: bool = attrs.field(default=False, validator=attrs.validators.instance_of(bool))

    def __str__(self) -> str:
        return self.name.replace("KEY", "")

    def __repr__(self) -> str:
        return f"<{self.name}: {self.value} (pressed={self.pressed})>"


@attrs.define(slots=True, kw_only=True)
class Keyboard:
    keymap: dict[str, Key] = attrs.field(
        factory=lambda: {f"KEY{i:X}": Key(name=f"KEY{i:X}", value=i) for i in range(16)}
    )

    def __getattr__(self, name: str) -> Key:
        if name in self.keymap:
            return self.keymap[name]
        raise AttributeError(f"Key '{name}' not found.")

    def is_key_pressed(self, value: int) -> bool:
        if 0 <= value < 16:
            return self.keymap[f"KEY{value:X}"].pressed
        raise ValueError(f"Key value {value} out of range (0-15).")

    @property
    def keys(self) -> list[list[Key]]:
        return [
            [self.KEY1, self.KEY2, self.KEY3, self.KEYC],
            [self.KEY4, self.KEY5, self.KEY6, self.KEYD],
            [self.KEY7, self.KEY8, self.KEY9, self.KEYE],
            [self.KEYA, self.KEY0, self.KEYB, self.KEYF],
        ]
