import pathlib
import sys
import os
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


def hex_to_square(directions: str) -> str:
    return directions.replace('nw', 'n').replace('se', 's')


def destination(directions: str) -> tuple[int, int]:
    north: int = directions.count('n') - directions.count('s')
    east: int = directions.count('e') - directions.count('w')
    return north, east


def black_tiles(tile_directions: list[str]) -> set[tuple[int, int]]:
    tile_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    for direction_str in tile_directions:
        tile: tuple[int, int] = destination(hex_to_square(direction_str))
        tile_counts[tile] += 1

    tiles: set[tuple[int, int]] = set()
    for position, count in tile_counts.items():
        if count % 2 == 1:
            tiles.add(position)
    return tiles


def neighbors(tile: tuple[int, int]) -> set[tuple[int, int]]:
    north, east = tile
    return {(north + 1, east),
            (north + 1, east + 1),
            (north, east - 1),
            (north, east + 1),
            (north - 1, east - 1),
            (north - 1, east)}


def update(tiles: set[tuple[int, int]]) -> set[tuple[int, int]]:
    whites_to_check: set[tuple[int, int]] = set()
    flipped_to_white: set[tuple[int, int]] = set()
    flipped_to_black: set[tuple[int, int]] = set()

    for tile in tiles:
        surrounding: set[tuple[int, int]] = neighbors(tile)
        whites_to_check.update(surrounding)
        if len(surrounding & tiles) not in (1, 2):
            flipped_to_white.add(tile)

    for tile in whites_to_check - tiles:
        if len(neighbors(tile) & tiles) == 2:
            flipped_to_black.add(tile)

    return (tiles | flipped_to_black) - flipped_to_white


def part1(data):
    """Solve part 1"""
    return len(black_tiles(data))


def part2(data):
    """Solve part 2"""
    tiles: set[tuple[int, int]] = black_tiles(data)
    for _ in range(100):
        tiles = update(tiles)
    return len(tiles)


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
