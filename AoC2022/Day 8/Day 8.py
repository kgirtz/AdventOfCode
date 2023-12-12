import pathlib
import sys
import os
from collections import namedtuple

Tree = namedtuple('Tree', 'x y h')


def parse(puzzle_input):
    """Parse input"""
    return [[int(d) for d in line] for line in puzzle_input.split('\n')]


def dimensions(patch: list[list[int]]) -> tuple[int, int]:
    return len(patch), len(patch[0])


def scenic_score(tree: Tree, patch: list[list[int]]) -> int:
    rows, cols = dimensions(patch)

    # Up
    up_view_dist: int = 0
    for y in range(tree.y - 1, -1, -1):
        up_view_dist += 1
        if patch[y][tree.x] >= tree.h:
            break

    # Down
    down_view_dist: int = 0
    for y in range(tree.y + 1, rows):
        down_view_dist += 1
        if patch[y][tree.x] >= tree.h:
            break

    # Left
    left_view_dist: int = 0
    for x in range(tree.x - 1, -1, -1):
        left_view_dist += 1
        if patch[tree.y][x] >= tree.h:
            break

    # Right
    right_view_dist: int = 0
    for x in range(tree.x + 1, cols):
        right_view_dist += 1
        if patch[tree.y][x] >= tree.h:
            break

    return up_view_dist * down_view_dist * left_view_dist * right_view_dist


def part1(data):
    """Solve part 1"""
    rows, cols = dimensions(data)

    visible: set[Tree] = set()

    # Top/Bottom
    for c in range(cols):
        # Top
        tallest: Tree = Tree(-1, -1, -1)
        for r in range(rows):
            h: int = data[r][c]
            if h > tallest.h:
                tallest = Tree(r, c, h)
                visible.add(tallest)

        # Bottom
        tallest: Tree = Tree(-1, -1, -1)
        for r in range(rows - 1, -1, -1):
            h: int = data[r][c]
            if h > tallest.h:
                tallest = Tree(r, c, h)
                visible.add(tallest)

    # Left/Right
    for r in range(rows):
        # Left
        tallest: Tree = Tree(-1, -1, -1)
        for c in range(cols):
            h: int = data[r][c]
            if h > tallest.h:
                tallest = Tree(r, c, h)
                visible.add(tallest)

        # Right
        tallest: Tree = Tree(-1, -1, -1)
        for c in range(cols - 1, -1, -1):
            h: int = data[r][c]
            if h > tallest.h:
                tallest = Tree(r, c, h)
                visible.add(tallest)

    return len(visible)


def part2(data):
    """Solve part 2"""
    rows, cols = dimensions(data)

    best_score: int = 0
    for y in range(rows):
        for x in range(cols):
            tree: Tree = Tree(x, y, data[y][x])
            best_score = max(best_score, scenic_score(tree, data))

    return best_score


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
