import pathlib
import sys
import os
from typing import NamedTuple, Self


class FabricSquare(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def left(self) -> int:
        return self.x

    def right(self) -> int:
        return self.x + self.width - 1

    def top(self) -> int:
        return self.y

    def bottom(self) -> int:
        return self.y + self.height - 1

    def points(self) -> set[tuple[int, int]]:
        pts: set[tuple[int, int]] = set()
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                pts.add((x, y))
        return pts

    def overlap(self, other: Self) -> Self | None:
        if self.right() < other.left() or self.left() > other.right() or \
           self.bottom() < other.top() or self.top() > other.bottom():
            return None

        left: int = max(self.left(), other.left())
        right: int = min(self.right(), other.right())
        top: int = max(self.top(), other.top())
        bottom: int = min(self.bottom(), other.bottom())
        return FabricSquare(left, top, right - left + 1, bottom - top + 1)


def parse(puzzle_input: str):
    """Parse input"""
    claims: list[tuple[int, FabricSquare]] = []
    for line in puzzle_input.split('\n'):
        id_num, _, pos, size = line.split()

        id_num = int(id_num.lstrip('#'))
        x, y = (int(n) for n in pos.rstrip(':').split(','))
        width, height = (int(n) for n in size.split('x'))

        claims.append((id_num, FabricSquare(x, y, width, height)))

    return claims


def part1(data):
    """Solve part 1"""
    duplicate_points: set[tuple[int, int]] = set()
    for i, (_, fs1) in enumerate(data[:-1]):
        for (_, fs2) in data[i + 1:]:
            overlap: FabricSquare | None = fs1.overlap(fs2)
            if overlap is not None:
                duplicate_points.update(overlap.points())
    return len(duplicate_points)


def part2(data):
    """Solve part 2"""
    for id1, fs1 in data:
        for id2, fs2 in data:
            if id1 == id2:
                continue
            if fs1.overlap(fs2) is not None:
                break
        else:
            return id1


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 4
    PART2_TEST_ANSWER = 3

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
