from drone import Drone
from abc import abstractmethod
from sys import argv
from typing import Optional, final
from string_distance import calculate_similarity
from drone import Drone

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
    drone = Drone(argv[1])
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

    @classmethod
    def execute(cls) -> None:
        cls.drone.finish(*cls.arguments)


class LoiterModeCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.set_mode("LOITER")


class LandModeCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.set_mode("LAND")


class StabilizeModeCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.set_mode("STABILIZE")


class GuidedModeCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.set_mode("GUIDED")


class ArmCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.arm(*cls.arguments)


class DisarmCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.disarm(*cls.arguments)


class TakeOffCommand(Command):
    def __init__(self):
        super().__init__(1)

    @classmethod
    def execute(cls) -> None:
        cls.drone.take_off(*cls.arguments)


class YawCommand(Command):
    def __init__(self):
        super().__init__(1)

    @classmethod
    def execute(cls) -> None:
        cls.drone.yaw(*cls.arguments)


class GoToCommand(Command):
    def __init__(self):
        super().__init__(2)

    @classmethod
    def execute(cls) -> None:
        cls.drone.goto(*cls.arguments)


class PrintInformationCommand(Command):
    def __init__(self):
        super().__init__(0)

    @classmethod
    def execute(cls) -> None:
        cls.drone.print_information(*cls.arguments)


class SetGroundSpeedCommand(Command):
    def __init__(self):
        super().__init__(1)

    @classmethod
    def execute(cls) -> None:
        cls.drone.set_ground_speed(*cls.arguments)


def preprocess(text: str) -> Optional[str]:
    similarity_scores = calculate_similarity(text.upper(), list_of_valid_commands)
    max_score = max(similarity_scores)
    max_index = similarity_scores.index(max_score)
    if max_score < 0.5:
        raise ValueError("unknown command")
    return max_index


def get_corresponding_command(preprocessed_text: str) -> Command:
    if preprocessed_text == list_of_valid_commands[0]:  # FINISH
        return FinishCommand()
    if preprocessed_text == list_of_valid_commands[1]:  # LOITER MODE
        return LoiterModeCommand()
    if preprocessed_text == list_of_valid_commands[2]:  # LAND MODE
        return LandModeCommand()
    if preprocessed_text == list_of_valid_commands[3]:  # STABILIZE MODE
        return StabilizeModeCommand()
    if preprocessed_text == list_of_valid_commands[4]:  # GUIDED MODE
        return GuidedModeCommand()
    if preprocessed_text == list_of_valid_commands[5]:  # ARM
        return ArmCommand()
    if preprocessed_text == list_of_valid_commands[6]:  # DISARM
        return DisarmCommand()
    if preprocessed_text == list_of_valid_commands[7]:  # TAKE OFF
        return TakeOffCommand()
    if preprocessed_text == list_of_valid_commands[8]:  # YAW
        return YawCommand()
    if preprocessed_text == list_of_valid_commands[9]:  # GOTO
        return GoToCommand()
    if preprocessed_text == list_of_valid_commands[10]:  # PRINT INFORMATION
        return PrintInformationCommand()
    if preprocessed_text == list_of_valid_commands[11]:  # SET GROUND SPEED
        return SetGroundSpeedCommand()


def transform_output(text: str) -> Command:
    preprocessed_text = preprocess(text)
    return get_corresponding_command(preprocessed_text)


def read_number(word: str) -> int:
    numbers = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        "hundred": 100,
        "thousand": 1000,
    }
    words = word.lower().replace("-", " ").split()
    number = 0
    temp_number = 0
    for word in words:
        if word == "and":
            continue
        if word in numbers:
            temp_number += numbers[word]
        elif word == "hundred":
            temp_number += 100
            number += temp_number * 1000
            temp_number = 0
        elif word == "thousand":
            temp_number *= 1000
            number += temp_number * 1000
            temp_number = 0
        else:
            raise ValueError("Invalid number")
    number += temp_number
    return number


def read_number(word: str) -> int:
    numbers = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        "hundred": 100,
        "thousand": 1000,
    }
    words = word.lower().replace("-", " ").split()
    number = 0
    temp_number = 0
    for word in words:
        if word == "and":
            continue
        if word == "hundred":
            if number == 0:
                number = 100
            else:
                number += temp_number * 100
                temp_number = 0
        elif word == "thousand":
            if number == 0:
                number = 1000
            else:
                number += temp_number * 1000
                temp_number = 0
        elif word in numbers:
            temp_number += numbers[word]
        else:
            raise ValueError("Invalid number")
    number += temp_number
    return number
