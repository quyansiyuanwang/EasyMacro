from typing import Self

from ..ThirdParty.RecognizerFramework.src.main import run as workflow_run
from .manager import Manager
from .monitor import KeyboardMonitor

keyboard_monitor = KeyboardMonitor()


class Trigger:
    def __init__(self, manager: Manager):
        self.manager: Manager = manager

    def load(self) -> Self:
        for _, macro in self.manager.macros.items():
            keyboard_monitor.add(
                macro.trigger,
                workflow_run,
                (macro.macro_json,),
            )
        return self

    def run(self):
        keyboard_monitor.run()

    def stop(self):
        keyboard_monitor.stop()
