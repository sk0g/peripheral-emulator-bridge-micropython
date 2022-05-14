import sys

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
# noinspection PyUnresolvedReferences
from second_core import pulse as p

micropython.alloc_emergency_exception_buf(100)


def toggle_pin(pin_number):
    pin_value = DeviceController.pin(pin_number).value
    DeviceController.pin(pin_number).set_value(0 if pin_value else 1)


def check_and_print_messages():
    # toggle_pin(14)
    # toggle_pin(25)
    if messages:
        print(f"{messages.pop()}")

    # TODO rewrite to use polling (select.poll) below
    # while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #     ch = sys.stdin.readline()
    #     print(ch)


def watch_deltas():
    Timer().init(
        period=500,
        mode=Timer.PERIODIC,
        callback=lambda t: check_and_print_messages(),
    )


for input_port in [2, 3]:  # input pins
    pi(input_port)
for output_port in [14, 25]:  # output pins
    po(output_port)

# init_second_core_task()

watch_deltas()
