import pathlib
import sys
import os
from collections import namedtuple, defaultdict

Point = namedtuple('Point', 'x y')

DIRECTIONS: list[str] = ['N', 'S', 'W', 'E']


def parse(puzzle_input):
    """Parse input"""
    elves: set[Point] = set()
    for y, line in enumerate(puzzle_input.split('\n')):
        for x, pos in enumerate(line):
            if pos == '#':
                elves.add(Point(x, y))
    return elves


def has_no_neighbor(elf: Point, elves: set[Point]) -> bool:
    neighbors: set[Point] = {Point(x, y) for x in range(elf.x - 1, elf.x + 2)
                                            for y in range(elf.y - 1, elf.y + 2)} - {elf}
    return len(neighbors & elves) == 0


def propose_single_move(elf: Point, elves: set[Point], direction: int) -> Point:
    if has_no_neighbor(elf, elves):
        return elf

    for _ in range(len(DIRECTIONS)):
        match DIRECTIONS[direction]:
            case 'N':
                if len(elves & {Point(x, elf.y - 1) for x in range(elf.x - 1, elf.x + 2)}) == 0:
                    return Point(elf.x, elf.y - 1)
            case 'S':
                if len(elves & {Point(x, elf.y + 1) for x in range(elf.x - 1, elf.x + 2)}) == 0:
                    return Point(elf.x, elf.y + 1)
            case 'W':
                if len(elves & {Point(elf.x - 1, y) for y in range(elf.y - 1, elf.y + 2)}) == 0:
                    return Point(elf.x - 1, elf.y)
            case 'E':
                if len(elves & {Point(elf.x + 1, y) for y in range(elf.y - 1, elf.y + 2)}) == 0:
                    return Point(elf.x + 1, elf.y)

        direction = (direction + 1) % len(DIRECTIONS)

    return elf


def propose_all_moves(elves: set[Point], first_direction: int) -> dict[Point, list[Point]]:
    moves: defaultdict[Point, list[Point]] = defaultdict(list)
    for elf in elves:
        move: Point = propose_single_move(elf, elves, first_direction)
        moves[move].append(elf)
    return moves


def move_elves(elves: set[Point], first_direction: int) -> set[Point]:
    new_positions: set[Point] = set()
    for dst, src in propose_all_moves(elves, first_direction).items():
        if len(src) == 1:
            new_positions.add(dst)
        else:
            new_positions.update(src)

    return new_positions


def empty_ground(elves: set[Point]) -> int:
    min_x: int = 0
    max_x: int = 0
    min_y: int = 0
    max_y: int = 0
    for x, y in elves:
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def part1(data):
    """Solve part 1"""
    elves: set[Point] = data
    for rd in range(10):
        elves = move_elves(elves, rd % len(DIRECTIONS))

    return empty_ground(elves)


def part2(data):
    """Solve part 2"""
    elves: set[Point] = data
    rd: int = 0
    while True:
        new_elves: set[Point] = move_elves(elves, rd % len(DIRECTIONS))
        rd += 1

        if new_elves == elves:
            return rd
        elves = new_elves


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
