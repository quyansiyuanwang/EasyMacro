from typing import Dict, Optional, Self

from ..Models.macro_json import Macro, MacroSet
from ..Util.utils import to_indent_str


class Manager:
    def __init__(self, path: Optional[str] = None) -> None:
        self._macros: MacroSet = MacroSet(macros={})

        if path is not None:
            self.load_file(path)

    def add_macro(self, name: str, macro: Macro):
        if name in self._macros.macros:
            raise ValueError(f"Macro with name '{name}' already exists.")
        self._macros.macros[name] = macro

    @property
    def macros(self) -> Dict[str, Macro]:
        return self._macros.macros

    def load_file(self, file_path: str) -> Self:
        with open(file_path, "r") as f:
            self._macros = MacroSet.from_json(f.read())
        return self

    def save_file(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(self._macros.model_dump_json(indent=4))

    def __repr__(self) -> str:
        return to_indent_str(self._macros.model_dump())
