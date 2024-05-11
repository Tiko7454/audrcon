from abc import abstractmethod
from typing import Optional, final


list_of_valid_commands = [
    "FINISH",
    "LOITER MODE",
    "LAND MODE",
    "STABILIZE MODE",
    "GUIDED MODE",
    "ARM",
    "DISARM",
    "TAKE OFF",
    "YAW",
    "GOTO",
    "PRINT INFORMATION",
    "SET GROUND SPEED",
]


class Command:
    head_command: Optional["Command"] = None
    arguments: list[int] = []

    def __init__(self, argument_number: int) -> None:
        self.argument_number = argument_number

    @classmethod
    @final
    def add_command(cls, command: "Command") -> None:
        cls.head_command = command

    @classmethod
    @final
    def add_argument(cls, argument: int) -> None:
        cls.arguments.append(argument)

    @classmethod
    @final
    def clean(cls) -> None:
        cls.head_command = None
        cls.arguments = []

    @classmethod
    @final
    def is_complete(cls) -> bool:
        assert cls.head_command
        return cls.head_command.argument_number == len(cls.arguments)

    @classmethod
    @abstractmethod
    def execute(cls) -> None:
        pass


def preprocess(text: str) -> str: ...


def get_corresponding_command(preprocessed_text: str) -> Command: ...


def transform_output(text: str) -> Command:
    preprocessed_text = preprocess(text)
    return get_corresponding_command(preprocessed_text)


def read_number(text: str) -> int: ...
