import pathlib
import sys
import os
from typing import Sequence
import numpy as np


def parse(puzzle_input):
    """Parse input"""
    return [int(d) for d in puzzle_input.strip()]


def convolve(signal: Sequence[int], pos: int) -> int:
    sum_len: int = pos + 1
    total: int = 0
    for i in range(pos, len(signal), 4 * sum_len):
        add_start: int = i
        add_end: int = i + sum_len
        sub_start: int = i + (2 * sum_len)
        sub_end: int = i + (3 * sum_len)
        total += sum(signal[add_start:add_end]) - sum(signal[sub_start:sub_end])

    # Return least significant digit of total
    return abs(total) % 10


def fft(signal: np.ndarray) -> None:
    signal_len: int = len(signal)

    # Accumulate sums from tail
    accumulated_signal: np.ndarray = signal.copy()
    for i in range(signal_len - 2, -1, -1):
        accumulated_signal[i] += accumulated_signal[i + 1]
    # accumulated_signal: np.ndarray = np.flip(np.cumsum(signal))

    # last_half: slice = slice(signal_len // 2, signal_len)
    # signal[last_half] = accumulated_signal[last_half]
    for i in range(signal_len // 2, signal_len):
        signal[i] = abs(accumulated_signal[i]) % 10

    # Modify sums with partial sums for all elements in first half of signal
    sign_pattern: list[int] = [1, 1, -1, -1]
    for frac in range(2, signal_len + 1):
        sign: int = sign_pattern[frac % 4]
        for i in range(signal_len // frac - 1, -1, -1):  # TODO: most time is spent here
            signal[i] += sign * accumulated_signal[frac * (i + 1) - 1]

    # Truncate to single digit
    # signal = np.abs(signal, out=signal)
    # signal %= 10
    for i, s in enumerate(signal[:signal_len // 2]):
        signal[i] = abs(s) % 10


def message(signal: Sequence[int], pos: int = 0) -> int:
    if pos + 7 < len(signal):
        return int(''.join(str(n) for n in signal[pos:pos + 8]))
    else:
        print(f'ERROR: Position too big - {pos} > {len(signal)}')
        return -1


def part1(data):
    """Solve part 1"""
    signal: np.ndarray = np.array(data)
    num_phases: int = 100

    for _ in range(num_phases):
        fft(signal)
    return message(signal)


def part2(data):
    """Solve part 2"""
    num_repetitions: int = 10000
    signal: np.ndarray = np.array(data * num_repetitions)
    num_phases: int = 100
    return ''

    for _ in range(num_phases):
        fft(signal)
        if _ % 10 == 0:
            print(_)
    return message(signal, int(''.join(str(n) for n in data[:7])))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
