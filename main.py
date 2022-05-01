from machine import Timer
from utime import ticks_us, sleep_us

from device import DeviceController as D, messages
from serial import process_line

import micropython

micropython.alloc_emergency_exception_buf(100)


def toggle_led():
    pin_value = D.pin(25).value
    D.pin(25).set_value(0 if pin_value else 1)


def x(command):
    process_line(command)


def check_and_print_messages():
    if messages:
        print(f"{messages.pop()}")


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

D.set_pin_data_direction(25, is_output=True)

D.set_pin_data_direction(2, is_output=False)

watch_deltas()
