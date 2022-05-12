import _thread

from utime import ticks_us, ticks_add, ticks_diff, sleep_us

from device import DeviceController

""" 
tasks stores lists in the format of [status, end_at_ns, on_pin]
status: 
    0 - not started
    1 - waiting
    2 - finished
end_at_us: 
    the time in microseconds to end this pulse at
on_pin: 
    the GPIO pin the pulse is running on
"""
tasks: list[list[int, int, int]] = []


def manage_pulses():
    global tasks

    while True:
        removable_indices = []
        for index, (status, end_at_us, on_pin) in enumerate(tasks):
            if status == 0:  # task is to be started
                DeviceController.pin(on_pin).set_value(1)
                tasks[index][0] = 1
                continue

            if status == 1 and ticks_diff(ticks_us(), end_at_us) >= 0:  # task has just completed
                DeviceController.pin(on_pin).set_value(0)
                tasks[index][0] = 2
                continue

            if status == 2:  # task is to be removed this tick
                removable_indices.append(index)
                continue

        for index in removable_indices:
            try:
                tasks.pop(index)
            except IndexError:
                continue

        sleep_us(100)


def pulse(pin_number: int, duration_ms: float):
    tasks.append([
        0,
        ticks_add(ticks_us(), int(duration_ms * 1e3)),
        pin_number,
    ])


def init_second_core_task():
    _thread.start_new_thread(manage_pulses, ())
