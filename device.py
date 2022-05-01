from machine import Pin

_formatted_pin_numbers = [f"{num}" if num > 10 else f"0{num}" for num in range(30)]

messages = set()
last_sent = {k: 0.5 for k in _formatted_pin_numbers}


def irq_handler(pin, pin_number):
    value = pin.value()
    if last_sent[pin_number] == value:
        return

    messages.add(f"{pin_number}|{value}")
    last_sent[pin_number] = value


class PinWrapper:
    pin = None
    number = None
    print_number = None
    is_output = None
    value = None

    def __init__(self, pin_number, is_output):
        self.pin = Pin(pin_number, Pin.OUT if is_output else Pin.IN)
        if not is_output:
            self.pin.init(pull=Pin.PULL_DOWN)

        self.pin.irq(lambda pin: irq_handler(pin, self.print_number))

        self.number = pin_number
        self.print_number = (str(self.number) if self.number > 9 else f"0{str(self.number)}")

        self.is_output = is_output

    def initialise(self, is_output):
        self.pin.init(mode=(Pin.OUT if is_output else Pin.IN))

        if not is_output:
            self.pin.init(pull=Pin.PULL_DOWN)

    def __str__(self):
        return f"{self.number},{'O' if self.is_output else 'I'},{self.get_value()}"

    def set_value(self, value):
        assert self.is_output

        self.pin.value(value)
        self.value = value

    def get_value(self):
        if not self.is_output:
            self.value = self.pin.value()

        return self.value


class DeviceController:
    pins = [None] * 27

    @staticmethod
    def pin(pin_number):
        return instance.pins[pin_number]

    @staticmethod
    def print_states():
        states = " | ".join([f"{pin}" for index, pin in enumerate(instance.pins) if pin])
        print(states)

    @staticmethod
    def set_pin_data_direction(pin_number, is_output):
        if not instance.pins[pin_number]:
            instance.pins[pin_number] = PinWrapper(pin_number, is_output=is_output)
            return

        instance.pins[pin_number].initialise(is_output)


instance = DeviceController()
