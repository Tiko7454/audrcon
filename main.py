from mic import record, output_filename
from recognize import recognize


while True:
    record()
    output = recognize(output_filename)
