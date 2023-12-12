import pathlib
import sys
import os

sys.path.append('..')
from intcode import IntcodeComputer


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def amplify_signal(phase_setting: list[int], intcode: list[int]) -> int:
    amplifiers: list[IntcodeComputer] = [IntcodeComputer() for _ in range(5)]
    signal = 0
    for phase, amplifier in zip(phase_setting, amplifiers):
        signal = amplifier.execute(intcode, [phase, signal])[0]
    return signal


def amplify_signal_feedback(phase_setting: list[int], intcode: list[int]) -> int:
    amplifiers: list[IntcodeComputer] = [IntcodeComputer() for _ in range(5)]
    signal = 0
    for phase, amplifier in zip(phase_setting, amplifiers):
        signal = amplifier.execute(intcode, [phase, signal])[0]

    i: int = 0
    while amplifiers[-1].state != 'HALTED':
        signal = amplifiers[i].run([signal])[0]
        i = (i + 1) % 5

    return signal


def permutations(arr: set[int]) -> list[list[int]]:
    if not arr:
        return [[]]

    perms: list[list[int]] = []
    for n in arr:
        for perm in permutations(arr - {n}):
            perms.append([n] + perm)
    return perms


def part1(data):
    """Solve part 1"""
    max_signal: int = 0
    for phase_setting in permutations({0, 1, 2, 3, 4}):
        max_signal = max(amplify_signal(phase_setting, data), max_signal)
    return max_signal


def part2(data):
    """Solve part 2"""
    max_signal: int = 0
    for phase_setting in permutations({5, 6, 7, 8, 9}):
        max_signal = max(amplify_signal_feedback(phase_setting, data), max_signal)
    return max_signal


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
