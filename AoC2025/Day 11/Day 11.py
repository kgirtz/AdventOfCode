import collections
import functools
from collections.abc import Mapping, Iterable

PART1_TEST_ANSWER = 5
PART2_TEST_ANSWER = 2


def parse(puzzle_input: str):
    devices: dict[str, set[str]] = {}
    for line in puzzle_input.split('\n'):
        k, v_str = line.split(':')
        v: set[str] = set(v_str.strip().split())
        devices[k.strip()] = v
    return devices


class ServerRack:
    def __init__(self, devices: Mapping[str, Iterable[str]]) -> None:
        self.inputs: dict[str, set[str]] = collections.defaultdict(set)
        for k, v in devices.items():
            for device in v:
                self.inputs[device].add(k)

    @functools.cache
    def unique_path_count(self, start: str, end: str, avoid: str = '') -> int:
        if start == end:
            return 1

        num_paths: int = 0
        for source in self.inputs[end]:
            if source != avoid:
                num_paths += self.unique_path_count(start, source, avoid)
        return num_paths


def part1(data):
    return ServerRack(data).unique_path_count('you', 'out')


def part2(data):
    rack: ServerRack = ServerRack(data)

    svr_fft: int = rack.unique_path_count('svr', 'fft', avoid='dac')
    svr_dac: int = rack.unique_path_count('svr', 'dac', avoid='fft')
    dac_fft: int = rack.unique_path_count('dac', 'fft')
    fft_dac: int = rack.unique_path_count('fft', 'dac')
    fft_out: int = rack.unique_path_count('fft', 'out', avoid='dac')
    dac_out: int = rack.unique_path_count('dac', 'out', avoid='fft')

    return svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out


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
