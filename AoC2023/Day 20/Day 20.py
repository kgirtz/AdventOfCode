import pathlib
import sys
import os
import abc
from typing import Iterable, Optional
from collections import deque


class Pulse:
    HIGH = True
    LOW = False

    def __init__(self, value: bool, sender: str, recipients: Iterable[str]) -> None:
        self.value: bool = value
        self.sender: str = sender
        self.recipients: tuple[str, ...] = tuple(recipients)


class Module(abc.ABC):
    def __init__(self, name: str, outputs: Iterable[str]) -> None:
        self.name: str = name
        self.outputs: tuple[str, ...] = tuple(outputs)
        self.pulse_queue: deque[Pulse] = deque()

    def ready(self) -> bool:
        return not self.pulse_queue

    def send_pulse(self, pulse: bool) -> Pulse:
        return Pulse(pulse, self.name, self.outputs)

    def receive_pulse(self, pulse: Pulse) -> None:
        self.pulse_queue.append(pulse)

    def get_next_pulse(self) -> Pulse:
        return self.pulse_queue.popleft()

    @abc.abstractmethod
    def process_next_pulse(self) -> Optional[Pulse]:
        pass


class Broadcaster(Module):
    def process_next_pulse(self) -> Optional[Pulse]:
        return self.send_pulse(self.get_next_pulse().value)


class FlipFlop(Module):
    ON = True
    OFF = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.state: bool = FlipFlop.OFF

    def process_next_pulse(self) -> Optional[Pulse]:
        if self.get_next_pulse().value == Pulse.LOW:
            self.state = not self.state
            return self.send_pulse(self.state)


class Conjunction(Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.last_input_pulse: dict[str, bool] = {}

    def add_input(self, new_input: str) -> None:
        self.last_input_pulse[new_input] = Pulse.LOW

    def process_next_pulse(self) -> Optional[Pulse]:
        pulse: Pulse = self.get_next_pulse()
        self.last_input_pulse[pulse.sender] = pulse.value
        return self.send_pulse(not all(self.last_input_pulse.values()))


def parse(puzzle_input):
    """Parse input"""
    modules: dict[str, Module] = {}
    conjunctions: dict[str, Conjunction] = {}
    for line in puzzle_input.split('\n'):
        name, destinations = line.split(' -> ')
        if name == 'broadcaster':
            modules[name] = Broadcaster(name, destinations.split(', '))
        elif name.startswith('%'):
            name = name[1:]
            modules[name] = FlipFlop(name, destinations.split(', '))
        elif name.startswith('&'):
            name = name[1:]
            conjunctions[name] = Conjunction(name, destinations.split(', '))
            modules[name] = conjunctions[name]

    for module in modules.values():
        for c in set(module.outputs) & conjunctions.keys():
            conjunctions[c].add_input(module.name)

    return modules


def push_button(modules: dict[str, Module]) -> (int, int, bool):
    modules['broadcaster'].receive_pulse(Pulse(Pulse.LOW, 'button', ['broadcaster']))
    low_count: int = 1
    high_count: int = 0
    low_to_rx: bool = False

    keep_processing: bool = True
    while keep_processing:
        keep_processing = False
        for module in modules.values():
            if module.ready():
                continue

            pulse: Optional[Pulse] = module.process_next_pulse()
            if pulse is None:
                continue

            keep_processing = True

            if pulse.value == Pulse.LOW:
                low_count += len(pulse.recipients)
            else:
                high_count += len(pulse.recipients)

            for recipient in pulse.recipients:
                if recipient in modules:
                    modules[recipient].receive_pulse(pulse)

    return low_count, high_count, low_to_rx


def part1(data):
    """Solve part 1"""
    low_total: int = 0
    high_total: int = 0
    for _ in range(1000):
        low_count, high_count, _ = push_button(data)
        low_total += low_count
        high_total += high_count
    return low_total * high_total


def part2(data):
    """Solve part 2"""
    _, _, rx_low = push_button(data)
    button_pushes: int = 1

    while not rx_low:
        _, _, rx_low = push_button(data)
        button_pushes += 1
        if button_pushes % 10000 == 0:
            print('.', end='')

    return button_pushes


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 11687500
    PART2_TEST_ANSWER = None

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()