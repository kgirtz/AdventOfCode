import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(line) for line in puzzle_input.split('\n')]


def transform(subject: int, loop_size: int) -> int:
    value: int = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value


def crack(subject: int, public_key: int) -> int:
    loop_size: int = 0
    value: int = 1
    while value != public_key:
        loop_size += 1
        value *= subject
        value %= 20201227
    return loop_size


def part1(data):
    """Solve part 1"""
    card_key, door_key = data
    card_loop_size: int = crack(7, card_key)
    door_loop_size: int = crack(7, door_key)

    encryption_key: int = transform(card_key, door_loop_size)
    assert encryption_key == transform(door_key, card_loop_size)
    return encryption_key


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
