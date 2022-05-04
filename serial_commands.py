import machine

from device import DeviceController

debug = True


def log(s: str):
    if debug:
        print(s)


def setup_input_pin(pin_number: int):
    log(f"Setting pin {pin_number} to input")
    DeviceController.set_pin_data_direction(
        pin_number=pin_number, is_output=False)


def setup_output_pin(pin_number: int):
    log(f"Setting pin {pin_number} to output")
    DeviceController.set_pin_data_direction(
        pin_number=pin_number, is_output=True)


def set_pin_on(pin_number: int):
    log(f"Update pin {pin_number} to value 1")
    DeviceController \
        .pin(pin_number) \
        .set_value(1)


def reset():
    log("Resetting...")
    machine.soft_reset()


def set_pin_off(pin_number: int):
    log(f"Update pin {pin_number} to value 0")
    DeviceController \
        .pin(pin_number) \
        .set_value(0)
