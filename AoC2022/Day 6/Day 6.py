import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.strip()


def start_of_marker(signal: str, marker_len: int) -> int:
    for pos in range(marker_len, len(signal)):
        marker: set[str] = set(signal[pos - marker_len:pos])
        if len(marker) == marker_len:
            return pos

    return 0


def part1(data):
    """Solve part 1"""

    return start_of_marker(data, 4)


def part2(data):
    """Solve part 2"""

    return start_of_marker(data, 14)


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
