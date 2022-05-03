import sys

from machine import Timer
import micropython
import select

from device import DeviceController, messages
from serial import process_line

micropython.alloc_emergency_exception_buf(100)


def toggle_led():
    pin_value = DeviceController.pin(25).value
    DeviceController.pin(25).set_value(0 if pin_value else 1)


def x(command):
    process_line(command)


def check_and_print_messages():
    if messages:
        print(f"{messages.pop()}")
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        print(ch)


def watch_deltas():
    print("start")

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
