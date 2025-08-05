from typing import Any, Dict, List, Union

from ..Typehints.basic import BaseObject


def to_indent_str(
    obj: Union[Dict[str, Any], List[BaseObject], BaseObject], level: int = 0
) -> str:
    pad = "  " * level

    if isinstance(obj, dict):
        if not obj:
            return "{}"

        items: List[str] = []
        for key, value in obj.items():
            formatted_value = to_indent_str(value, level + 1)
            items.append(f"{pad}  {key}: {formatted_value}")

        return "{\n" + ",\n".join(items) + f"\n{pad}}}"

    elif isinstance(obj, list):
        if not obj:
            return "[]"

        items = []
        has_complex_items = any(isinstance(item, dict) for item in obj)

        for item in obj:
            items.append(
                f"{pad}  {to_indent_str(item, level + 1)}"
                if isinstance(item, dict)
                else repr(item)
            )

        if has_complex_items:
            return "[\n" + ",\n".join(items) + f"\n{pad}]"
        return "[" + ", ".join(items) + "]"

    elif isinstance(obj, str):
        return f"'{obj}'"

    return repr(obj)
