import pathlib
import sys
import os

points = set[tuple[int, int]]


def parse(puzzle_input):
    """Parse input"""
    floor: list[str] = puzzle_input.split('\n')
    x_len: int = len(floor[0])
    y_len: int = len(floor)
    east: points = set()
    south: points = set()
    for y, row in enumerate(floor):
        for x, space in enumerate(row):
            if space == '>':
                east.add((x, y))
            elif space == 'v':
                south.add((x, y))
    return x_len, y_len, east, south


def moveable(direction: str, east: points, south: points, x_len: int, y_len: int) -> tuple[points, points]:
    sources: points = set()
    destinations: points = set()
    combined: points = east | south

    if direction == '>':
        for x, y in east:
            dst: tuple[int, int] = (x + 1) % x_len, y
            if dst not in combined:
                sources.add((x, y))
                destinations.add(dst)
    else:
        for x, y in south:
            dst: tuple[int, int] = x, (y + 1) % y_len
            if dst not in combined:
                sources.add((x, y))
                destinations.add(dst)

    return sources, destinations


def move_east(east: points, south: points, x_len: int, y_len: int) -> bool:
    old_spots, new_spots = moveable('>', east, south, x_len, y_len)
    east.update(new_spots)
    for cucumber in old_spots:
        east.remove(cucumber)
    return len(new_spots) != 0


def move_south(east: points, south: points, x_len: int, y_len: int) -> bool:
    old_spots, new_spots = moveable('v', east, south, x_len, y_len)
    south.update(new_spots)
    for cucumber in old_spots:
        south.remove(cucumber)
    return len(new_spots) != 0


def step(east: points, south: points, x_len: int, y_len: int) -> bool:
    moved: bool = False
    if move_east(east, south, x_len, y_len):
        moved = True
    if move_south(east, south, x_len, y_len):
        moved = True
    return moved


def part1(data):
    """Solve part 1"""
    x_len, y_len, east, south = data
    steps: int = 1
    while step(east, south, x_len, y_len):
        steps += 1
    return steps


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
