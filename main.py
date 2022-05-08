import sys

import utime
from machine import Timer
import micropython
import select

from device import DeviceController, messages

# noinspection PyUnresolvedReferences
from serial_commands import (
    setup_input_pin as pi,
    setup_output_pin as po,
    set_pin_on as n,
    set_pin_off as f,
    reset as r,
)

micropython.alloc_emergency_exception_buf(100)


def toggle_led():
    pin_value = DeviceController.pin(25).value
    DeviceController.pin(25).set_value(0 if pin_value else 1)


def check_and_print_messages():
    if messages:
        print(f"{messages.pop()}")
    # TODO rewrite to use polling (select.poll) below
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        print(ch)


def watch_deltas():
    Timer().init(
        period=1,
        mode=Timer.PERIODIC,
        callback=lambda t: check_and_print_messages(),
    )


# Timer().init(
#     period=5000,
#     mode=Timer.PERIODIC,
#     callback=lambda t: toggle_led()
# )

# DeviceController.set_pin_data_direction(25, is_output=True)

DeviceController.set_pin_data_direction(2, is_output=False)

watch_deltas()
