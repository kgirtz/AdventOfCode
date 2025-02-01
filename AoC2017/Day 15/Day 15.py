from collections.abc import Generator

PART1_TEST_ANSWER = 588
PART2_TEST_ANSWER = 309


def parse(puzzle_input: str):
    return [int(line.split()[-1]) for line in puzzle_input.split('\n')]


def generator(starting_value: int, factor: int, divisor: int = 1) -> Generator[int]:
    value: int = starting_value
    while True:
        if value % divisor == 0:
            yield value
        value *= factor
        value %= 2147483647


def num_matches(gen_a: Generator[int], gen_b: Generator[int], num_pairs: int) -> int:
    return sum(next(gen_a) & 0xFFFF == next(gen_b) & 0xFFFF for _ in range(num_pairs))


def part1(data):
    starting_a, starting_b = data
    factor_a, factor_b = (16807, 48271)
    return num_matches(generator(starting_a, factor_a),
                       generator(starting_b, factor_b),
                       40000000)


def part2(data):
    starting_a, starting_b = data
    factor_a, factor_b = (16807, 48271)
    divisor_a, divisor_b = (4, 8)
    return num_matches(generator(starting_a, factor_a, divisor_a),
                       generator(starting_b, factor_b, divisor_b),
                       5000000)


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
