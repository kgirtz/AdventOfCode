from collections.abc import Iterable, Mapping

PART1_TEST_ANSWER = 5
PART2_TEST_ANSWER = 2


def parse(puzzle_input: str):
    devices: dict[str, set[str]] = {}
    for line in puzzle_input.split('\n'):
        k, v_str = line.split(':')
        v: set[str] = set(v_str.strip().split())
        devices[k.strip()] = v
    return devices


def all_paths_between(start: str, end: str, devices: Mapping[str, Iterable[str]], *, must_pass: Iterable[str] = tuple()) -> list[list[str]]:
    complete_paths: list[list[str]] = []
    partial_paths: list[list[str]] = [[start]]
    while partial_paths:
        new_partials: list[list[str]] = []
        for p in partial_paths:
            for next_device in devices[p[-1]]:
                new_p: list[str] = p + [next_device]
                if next_device == end:
                    if all(d in new_p for d in must_pass):
                        complete_paths.append(new_p)
                elif next_device not in p:
                    new_partials.append(new_p)
        partial_paths = new_partials
    return complete_paths


def part1(data):
    return len(all_paths_between('you', 'out', data))


def part2(data):
    return len(all_paths_between('svr', 'out', data, must_pass=('fft', 'dac')))


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
