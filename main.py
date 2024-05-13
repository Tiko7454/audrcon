from drone import Drone
from mic import record, output_filename
from recognize import recognize
from command import transform_output, Command, read_number


while True:
    record()
    output = recognize(output_filename)
    print(output)
    if not Command.head_command:
        command = transform_output(output)
        Command.add_command(command)
    else:
        number = read_number(output)
        Command.add_argument(number)
    if Command.is_complete():
        assert Command.head_command
        Command.head_command.execute()
        Command.clean()
