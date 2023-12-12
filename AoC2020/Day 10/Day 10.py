import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def deltas(stream: list[int]) -> list[int]:
    diffs: list[int] = []
    for i in range(1, len(stream)):
        diffs.append(stream[i] - stream[i - 1])
    return diffs


def part1(data):
    """Solve part 1"""
    joltages: list[int] = [0] + sorted(data) + [max(data) + 3]
    diffs: list[int] = deltas(joltages)
    return diffs.count(1) * diffs.count(3)


def part2(data):
    """Solve part 2"""
    joltages: list[int] = [0] + sorted(data) + [max(data) + 3]
    diffs: list[int] = deltas(joltages)
    arrangements: list[int] = [0] * len(joltages)
    arrangements[0] = 1
    for i in range(len(diffs)):
        for j in range(i - 2, i + 1):
            if j >= 0 and sum(diffs[j:i + 1]) <= 3:
                arrangements[i + 1] += arrangements[j]
    return arrangements[-1]


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
