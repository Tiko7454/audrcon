from abc import abstractmethod
from typing import Optional, final
from string_distance import calculate_similarity

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


class FinishCommand(Command):
    def __init__(self):
        super().__init__(0)


class LoiterModeCommand(Command):
    def __init__(self):
        super().__init__(0)


class LandModeCommand(Command):
    def __init__(self):
        super().__init__(0)


class StabilizeModeCommand(Command):
    def __init__(self):
        super().__init__(0)


class GuidedModeCommand(Command):
    def __init__(self):
        super().__init__(0)


class ArmCommand(Command):
    def __init__(self):
        super().__init__(0)


class DisarmCommand(Command):
    def __init__(self):
        super().__init__(0)


class TakeOffCommand(Command):
    def __init__(self):
        super().__init__(1)


class YawCommand(Command):
    def __init__(self):
        super().__init__(1)


class GoToCommand(Command):
    def __init__(self):
        super().__init__(2)


class PrintInformationCommand(Command):
    def __init__(self):
        super().__init__(0)


class SetGroundSpeedCommand(Command):
    def __init__(self):
        super().__init__(1)


def preprocess(text: str) -> Optional[str]:
    similarity_scores = calculate_similarity(text.upper(), list_of_valid_commands)
    max_score = max(similarity_scores)
    max_index = similarity_scores.index(max_score)
    return max_index if max_score > 0.5 else raise Exception("Please try again.")


def get_corresponding_command(preprocessed_text: str) -> Command:
    if preprocessed_text == list_of_valid_commands[0]: # FINISH
        return FinishCommand()
    if preprocessed_text == list_of_valid_commands[1]: # LOITER MODE
        return LoiterModeCommand()
    if preprocessed_text == list_of_valid_commands[2]: # LAND MODE
        return LandModeCommand()
    if preprocessed_text == list_of_valid_commands[3]: # STABILIZE MODE
        return StabilizeModeCommand()
    if preprocessed_text == list_of_valid_commands[4]: # GUIDED MODE
        return GuidedModeCommand()
    if preprocessed_text == list_of_valid_commands[5]: # ARM
        return ArmCommand()
    if preprocessed_text == list_of_valid_commands[6]: # DISARM
        return DisarmCommand()
    if preprocessed_text == list_of_valid_commands[7]: # TAKE OFF
        return TakeOffCommand()
    if preprocessed_text == list_of_valid_commands[8]: # YAW
        return YawCommand()
    if preprocessed_text == list_of_valid_commands[9]: # GOTO
        return GoToCommand()
    if preprocessed_text == list_of_valid_commands[10]: # PRINT INFORMATION
        return PrintInformationCommand()
    if preprocessed_text == list_of_valid_commands[11]: # SET GROUND SPEED
        return SetGroundSpeedCommand()


def transform_output(text: str) -> Command:
    preprocessed_text = preprocess(text)
    return get_corresponding_command(preprocessed_text)


def read_number(text: str) -> int: ...
