from collections.abc import Sequence

PART1_TEST_ANSWER = 52432133
PART2_TEST_ANSWER = 53553731


def parse(puzzle_input):
    """Parse input"""
    return [int(d) for d in puzzle_input.strip()]


def convolve(signal: Sequence[int], position: int) -> int:
    sum_len: int = position + 1
    total: int = 0
    for i in range(position, len(signal), 4 * sum_len):
        add_start: int = i
        add_end: int = i + sum_len
        sub_start: int = i + (2 * sum_len)
        sub_end: int = i + (3 * sum_len)
        total += sum(signal[add_start:add_end]) - sum(signal[sub_start:sub_end])
    return abs(total) % 10


def fft(signal: Sequence[int]) -> list[int]:
    return [convolve(signal, n) for n in range(len(signal))]


def fft_last_half(signal: Sequence[int]) -> list[int]:
    tail_accumulations: list[int] = list(signal)
    for i in range(len(signal) - 2, -1, -1):
        tail_accumulations[i] = (tail_accumulations[i] + tail_accumulations[i + 1]) % 10
    return tail_accumulations


def message(signal: Sequence[int], offset: int = 0) -> int:
    if not (0 <= offset < len(signal)):
        raise IndexError('invalid message offset')
    return int(''.join(str(n) for n in signal[offset:offset + 8]))


def part1(data):
    """Solve part 1"""
    signal: Sequence[int] = data
    for _ in range(100):
        signal = fft(signal)
    return message(signal)


def part2(data):
    """Solve part 2"""
    repetitions: int = 10000
    signal: list[int] = list(data)
    message_offset: int = int(''.join(str(n) for n in signal[:7]))
    repetitions -= message_offset // len(signal) + 1
    message_offset %= len(signal)
    signal = signal[message_offset:] + signal * repetitions
    for _ in range(100):
        signal = fft_last_half(signal)
    return message(signal)


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
