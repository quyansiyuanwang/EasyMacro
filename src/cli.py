import argparse
import sys

from .Core.manager import Manager
from .Core.trigger import Trigger


def load_macros(path: str):
    trigger = Trigger(Manager(path))
    trigger.load().run()


def input_macros() -> str:
    path = input(
        "Enter the path to the macros JSON file (default: macros/register.json): "
    )
    if not path.strip():
        raise ValueError("Path cannot be empty.")
    return path


def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EasyMacro CLI")
    parser.add_argument(
        "macros",
        type=str,
        help="Path to the macros json file to load",
    )
    args: argparse.Namespace = parser.parse_args(sys.argv[1:])

    if not args.macros:
        args.macros = input_macros()

    return args


def cli() -> None:
    args = args_parse()
    load_macros(args.macros)


__all__ = [
    "load_macros",
    "cli",
]
