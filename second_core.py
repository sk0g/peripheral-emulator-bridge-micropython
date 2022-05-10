import _thread

import utime

from device import DeviceController

semaphore = _thread.allocate_lock()


def pulse_pin(pin_number: int, duration: int):
    semaphore.acquire()
    DeviceController.pin(pin_number).set_value(1)

    utime.sleep_us(duration)

    DeviceController.pin(pin_number).set_value(0)
    semaphore.release()


def pulse(pin_number: int, duration_ms: float):
    _thread.start_new_thread(pulse_pin, (pin_number, int(duration_ms * 1000)))
