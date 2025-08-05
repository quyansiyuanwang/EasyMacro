import threading
from typing import Any, Callable, Dict, List, Optional, Self, Tuple, TypeAlias, Union

import keyboard
from pydantic import BaseModel, Field

HandlerType: TypeAlias = Callable[[], None]
CallbackType: TypeAlias = Callable[..., Any]
ArgsType: TypeAlias = Tuple[Any, ...]
KeyTypes: TypeAlias = Union[str, List[str]]


def _thread_closure(callback: CallbackType, args: ArgsType) -> HandlerType:
    def handler() -> None:
        thread = threading.Thread(target=callback, args=args)
        thread.daemon = True
        thread.start()

    return handler


class CallbackPack(BaseModel):
    """A pack of callback functions for a hotkey."""

    callback: CallbackType = Field(default_factory=lambda: lambda: None)
    args: ArgsType = Field(default_factory=tuple)


class KeyboardMonitor:
    _total_monitor: List["KeyboardMonitor"] = list()

    def __init__(
        self, enable_thread: bool = True, on_exit: Optional[str] = "ctrl+c"
    ) -> None:
        self._total_monitor.append(self)
        self._handlers: Dict[str, List[HandlerType]] = {}
        self._pendings: Dict[str, List[CallbackPack]] = {}
        self._enable_thread: bool = enable_thread

        self._is_running: bool = False

        if on_exit:
            self.add(on_exit, lambda: self.stop(), ())

    def parse_hotkey(self, hotkey: KeyTypes) -> str:
        if isinstance(hotkey, list):
            return "+".join(hotkey)
        return hotkey

    def add(self, hotkey: KeyTypes, callback: CallbackType, args: ArgsType) -> None:
        hotkey = self.parse_hotkey(hotkey)
        self._pendings.setdefault(hotkey, []).append(
            CallbackPack(callback=callback, args=args)
        )

    def adds(
        self, hotkeys: List[KeyTypes], callback: CallbackType, args: ArgsType
    ) -> None:
        for hotkey in hotkeys:
            self.add(hotkey=hotkey, callback=callback, args=args)

    def register(
        self, hotkey: KeyTypes, args: ArgsType = ()
    ) -> Callable[[CallbackType], CallbackType]:
        hotkey = self.parse_hotkey(hotkey=hotkey)

        def inner(callback: CallbackType) -> CallbackType:
            self.add(hotkey=hotkey, callback=callback, args=args)
            return callback

        return inner

    def unregister(self, hotkey: KeyTypes) -> Self:
        hotkey = self.parse_hotkey(hotkey=hotkey)
        if hotkey in list(self._pendings.keys()):
            del self._pendings[hotkey]

        if hotkey in self._handlers:
            self.off_key(hotkey)

        return self

    def reload(self) -> Self:
        """Reload the keyboard listener."""
        self.off_all()
        self.on_all()
        return self

    def get_total_monitor_num(self) -> int:
        return len(self._total_monitor)

    def on(
        self, hotkey: KeyTypes, callback: CallbackType, args: ArgsType
    ) -> HandlerType:
        """Register a hotkey to the keyboard listener."""
        if not self._is_running:
            raise RuntimeError("KeyboardMonitor is not running. Call run() first.")
        hotkey = self.parse_hotkey(hotkey)

        if self._enable_thread:
            callback = _thread_closure(callback, args)
            args = ()

        hotkey_handler = keyboard.add_hotkey(
            hotkey=hotkey,
            callback=callback,
            args=args,
        )
        self._handlers.setdefault(hotkey, []).append(hotkey_handler)
        return hotkey_handler

    def on_key(self, hotkey: KeyTypes) -> List[HandlerType]:
        """Register a hotkey to the keyboard listener."""
        if not self._is_running:
            raise RuntimeError("KeyboardMonitor is not running. Call run() first.")
        hotkey = self.parse_hotkey(hotkey)
        ret: List[HandlerType] = []
        for pkg in self._pendings.get(hotkey, []):
            ret.append(self.on(hotkey=hotkey, callback=pkg.callback, args=pkg.args))
        return ret

    def on_all(self) -> None:
        for hotkey, callbacks in self._pendings.items():
            for callback in callbacks:
                self.on(hotkey=hotkey, callback=callback.callback, args=callback.args)

    def off(self, handler: HandlerType) -> Self:
        if not self._is_running:
            raise RuntimeError("KeyboardMonitor is not running. Call run() first.")
        keyboard.remove_hotkey(handler)
        return self

    def off_key(self, hotkey: KeyTypes) -> Self:
        """Unregister a hotkey from the keyboard listener."""
        hotkey = self.parse_hotkey(hotkey)
        if hotkey in self._handlers:
            for handler in self._handlers[hotkey]:
                keyboard.remove_hotkey(handler)
            del self._handlers[hotkey]

        return self

    def off_all(self) -> None:
        for hotkey in list(self._handlers.keys()):
            self.off_key(hotkey)

    def run(self) -> None:
        self._is_running = True
        self.on_all()
        while self._is_running:
            keyboard.wait()

    def stop(self) -> None:
        """Stop the keyboard listener."""
        if not self._is_running:
            raise RuntimeError("KeyboardMonitor is not running. Call run() first.")
        self.off_all()
        self._is_running = False
