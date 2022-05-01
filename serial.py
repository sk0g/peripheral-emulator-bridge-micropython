import re

import machine

uart_selected = 1
uart_baud_rate = 115200
uart_bits = 8
uart_parity_bits = None
uart_stop_bits = 1
uart_timeout = 2000

value_update = re.compile("(\d{1,2})\|(\d\.?\d{0,2})")
set_port_direction = re.compile("P\|(\d{1,2})")


def process_port_set(matches):
    print(f"Processing port set with {matches=}")


def send_value(matches):
    print(f"Sending value to port with {matches=}")


def receive_value(line: str):
    split = line.split("|")

    if len(split) <= 1:
        print(f"Splitting receive value command with malformed {line=}")

    port_num = int(split[0])
    value = float(split[1])

    print(f"Received {value=} from {port_num=}")


def process_line(line: str):
    print(f"Processing {line=}")

    if line == "reset":
        print("resetting")
        machine.reset()

    elif (m := value_update.match(line)):
        send_value(m)

    elif (m := set_port_direction.match(line)):
        process_port_set(m)
