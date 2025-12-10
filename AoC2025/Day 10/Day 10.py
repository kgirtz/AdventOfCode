from collections.abc import Sequence

PART1_TEST_ANSWER = 7
PART2_TEST_ANSWER = 33


class Machine:
    def __init__(self, lights: str, buttons: str, joltages: str) -> None:
        self.lights: list[bool] = [light == '#' for light in lights]
        self.buttons: list[tuple[int, ...]] = []
        self.joltages: list[int] = [int(j) for j in joltages.split(',')]

        for button in buttons.strip().split():
            button = button.lstrip('(').rstrip(')')
            self.buttons.append(tuple(int(b) for b in button.split(',')))

    def fewest_button_presses_lights(self) -> int:
        fewest: dict[tuple[bool, ...], int] = {}
        edge: set[tuple[bool, ...]] = {tuple(False for _ in self.lights)}
        distance: int = 0
        while edge:
            new_edge: set[tuple[bool, ...]] = set()
            for state in edge:
                fewest[state] = distance
                for button in self.buttons:
                    next_state: tuple[bool, ...] = update_lights(state, button)
                    if next_state not in fewest and next_state not in edge:
                        new_edge.add(next_state)

            edge = new_edge
            distance += 1

        return fewest[tuple(self.lights)]

    def fewest_button_presses_joltages(self) -> int:
        fewest: dict[tuple[int, ...], int] = {}
        edge: set[tuple[int, ...]] = {tuple(0 for _ in self.joltages)}
        distance: int = 0
        while edge:
            new_edge: set[tuple[int, ...]] = set()
            for state in edge:
                fewest[state] = distance
                for button in self.buttons:
                    next_state: tuple[int, ...] = update_joltages(state, button)
                    if next_state not in fewest and next_state not in edge:
                        if all(n <= j for n, j in zip(next_state, self.joltages)):
                            new_edge.add(next_state)

            edge = new_edge
            distance += 1

        return fewest[tuple(self.joltages)]


def update_lights(lights: Sequence[bool], button_pressed: tuple[int, ...]) -> tuple[bool, ...]:
    lights = list(lights)
    for i in button_pressed:
        lights[i] ^= True
    return tuple(lights)


def update_joltages(joltages: Sequence[int], button_pressed: tuple[int, ...]) -> tuple[int, ...]:
    joltages = list(joltages)
    for i in button_pressed:
        joltages[i] += 1
    return tuple(joltages)


def parse(puzzle_input: str):
    machines: list[Machine] = []
    for line in puzzle_input.split('\n'):
        light_str, line = line.split(']')
        light_str = light_str.strip().lstrip('[')

        button_str, joltage_str = line.strip().split('{')
        button_str = button_str.strip()
        joltage_str = joltage_str.strip().rstrip('}')

        machines.append(Machine(light_str, button_str, joltage_str))

    return machines


def part1(data):
    return sum(machine.fewest_button_presses_lights() for machine in data)


def part2(data):
    return sum(machine.fewest_button_presses_joltages() for machine in data)


# ------------- DO NOT MODIFY BELOW THIS LINE ------------- #


import pathlib


def get_puzzle_input(file: pathlib.Path) -> str:
    if not file.exists():
        return ''
    return file.read_text().strip('\n').replace('\t', ' ' * 4)


def execute(func, puzzle_input: str) -> (..., int):
    import time

    start: int = time.perf_counter_ns()
    result = func(parse(puzzle_input))
    execution_time_us: int = (time.perf_counter_ns() - start) // 1000
    return result, execution_time_us


def timestamp(execution_time_us: int) -> str:
    stamp: str = f'{round(execution_time_us / 1000000, 3)} s'
    if execution_time_us < 1000000:
        stamp = f'{round(execution_time_us / 1000, 3)} ms'
    return f'\t[{stamp}]'


def test(part_num: int, directory: str) -> None:
    if part_num == 1:
        func = part1
        answer = PART1_TEST_ANSWER
    else:
        func = part2
        answer = PART2_TEST_ANSWER

    prefix: str = f'PART {part_num} TEST: '
    if answer is None:
        print(prefix + 'skipped')
        return

    file: pathlib.Path = pathlib.Path(directory, f'part{part_num}_test.txt')
    if not file.exists():
        file = pathlib.Path(directory, 'test.txt')

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    result = 'PASS' if result == answer else 'FAIL'
    print(prefix + result + timestamp(duration))


def solve(part_num: int, directory: str) -> None:
    func = part1 if part_num == 1 else part2
    prefix: str = f'PART {part_num}: '

    file: pathlib.Path = pathlib.Path(directory, 'input.txt')
    if not file.exists():
        # Download file?
        ...

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    suffix: str = '' if result is None else timestamp(duration)
    print(prefix + str(result) + suffix)


if __name__ == '__main__':
    import os

    working_directory: str = os.path.dirname(__file__)

    test(1, working_directory)
    test(2, working_directory)
    print()
    solve(1, working_directory)
    solve(2, working_directory)
