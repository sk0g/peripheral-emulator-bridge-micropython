import re

from device import DeviceController

import machine

uart_selected = 1
uart_baud_rate = 115200
uart_bits = 8
uart_parity_bits = None
uart_stop_bits = 1
uart_timeout = 2000

value_update = re.compile(r'(\d\d)\|(\d)')
set_port_input = re.compile(r'PI\|(\d\d)')
set_port_output = re.compile(r'PO\|(\d\d)')


def process_port_set(matches, is_input: bool):
    print(f"Processing port set with {matches.groups()=}, {is_input=}")
    DeviceController.set_pin_data_direction(
        pin_number=int(matches.group(1)),
        is_output=not is_input)


def set_value(matches):
    print(f"Sending value to port with {matches=}")
    DeviceController \
        .pin(int(matches.group(1))) \
        .set_value(int(matches.group(2)))


def process_line(line: str):
    line = line.strip()
    print(f"Processing {line=}")

    if line == "reset":
        print("resetting")
        machine.reset()

    elif m := value_update.match(line):
        set_value(m)

    elif m := set_port_input.match(line):
        process_port_set(m, is_input=True)

    elif m := set_port_output.match(line):
        process_port_set(m, is_input=False)

    else:
        print(f"unrecognised command {list(line)}")
