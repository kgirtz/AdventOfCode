import functools
from collections.abc import Iterable, Set
from typing import TypeAlias

PART1_TEST_ANSWER = 31
PART2_TEST_ANSWER = 19

Component: TypeAlias = tuple[int, ...]


def parse(puzzle_input: str):
    return [tuple(int(n) for n in line.split('/')) for line in puzzle_input.split('\n')]


@functools.cache
def strongest_bridge(open_port: int, components: Set[Component]) -> list[Component]:
    connectable: list[Component] = [comp for comp in components if open_port in comp]
    if not connectable:
        return []

    max_strength: int = 0
    max_bridge: list[Component] = []
    for comp in connectable:
        other_port: int = comp[1] if comp[0] == open_port else comp[0]
        remaining_components: frozenset[Component] = frozenset(components - {comp})
        sub_bridge: list[Component] = [comp] + strongest_bridge(other_port, remaining_components)
        sub_strength: int = strength(sub_bridge)
        if sub_strength > max_strength:
            max_strength = sub_strength
            max_bridge = sub_bridge

    return max_bridge


@functools.cache
def longest_bridge(open_port: int, components: Set[Component]) -> list[Component]:
    connectable: list[Component] = [comp for comp in components if open_port in comp]
    if not connectable:
        return []

    long_bridge: list[Component] = []
    for comp in connectable:
        other_port: int = comp[1] if comp[0] == open_port else comp[0]
        remaining_components: frozenset[Component] = frozenset(components - {comp})
        sub_bridge: list[Component] = [comp] + longest_bridge(other_port, remaining_components)
        if len(sub_bridge) > len(long_bridge) or (len(sub_bridge) == len(long_bridge) and
                                                  strength(sub_bridge) > strength(long_bridge)):
            long_bridge = sub_bridge

    return long_bridge


def strength(bridge: Iterable[Component]) -> int:
    return sum(sum(component) for component in bridge)


def part1(data):
    return strength(strongest_bridge(0, frozenset(data)))


def part2(data):
    return strength(longest_bridge(0, frozenset(data)))


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
