from typing import Callable


class Command:
    def __init__(self, name: str, handler: Callable, min_args: int, max_args: int, help_text: str):
        self.name = name
        self.handler = handler
        self.min_args = min_args
        self.max_args = max_args
        self.help_text = help_text