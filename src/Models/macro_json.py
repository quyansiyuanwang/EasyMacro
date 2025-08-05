from typing import Dict, List, Self, Union

from pydantic import BaseModel, Field


class Macro(BaseModel):
    description: str = Field(str(), description="Description of the macro")
    macro_json: str = Field(..., description="Path of the macro JSON file")
    trigger: List[Union[str, List[str]]] = Field(
        ..., description="List of triggers for the macro"
    )

    @classmethod
    def from_json(cls, json_data: str) -> Self:
        """Create a Macro instance from JSON data."""
        return cls.model_validate_json(json_data)


class MacroSet(BaseModel):
    macros: Dict[str, Macro] = Field(..., description="List of macros in the macro set")

    @classmethod
    def from_json(cls, json_data: str) -> Self:
        """Create a MacroSet instance from JSON data."""
        return cls.model_validate_json(json_data)
