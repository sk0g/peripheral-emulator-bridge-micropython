import utime

SLEEP_BETWEEN_LOOPS_US = 50

current_time_us: int = 0
tasks: list["CoreTask"] = []


class CoreTask:
    till_time_us: int
    port_number: int
    started: bool = False

    def __init__(self, port_number, duration_us):
        self.port_number = port_number
        self.till_time_us = current_time_us + duration_us

    def is_done(self) -> bool:
        return current_time_us >= self.till_time_us

    def cleanup(self):
        # turn port off
        pass


def add_task(port_num: int, duration_us: int):
    tasks.append(CoreTask(port_num, duration_us))


def core_task():
    global current_time_us
    while True:
        # Update time_us
        current_time_us = utime.time_ns() * 1000

        completed_task_indices = []
        # Loop over current tasks, looking for ones that are completed
        for index, task in enumerate(tasks):
            if task.is_done():
                completed_task_indices.append(index)
                task.cleanup()

        # Remove any completed tasks
        for index in completed_task_indices:
            tasks.pop(index)

        # Sleep
        utime.sleep_us(min(
            10,
            SLEEP_BETWEEN_LOOPS_US - ((utime.time_ns() * 1000) - current_time_us)
        ))