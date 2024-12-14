import pathlib
import sys
import os
import functools
import heapq
from xypair import XYpair
from collections import defaultdict


class HeatLossMap:
    def __init__(self, heat_loss_map: list[list[int]]) -> None:
        self.height: int = len(heat_loss_map)
        self.width: int = len(heat_loss_map[0])
        self.heat_loss: list[list[int]] = heat_loss_map
        self.inf: int = sum(sum(row) for row in heat_loss_map)

    def __contains__(self, pt: XYpair) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def heat_loss_at(self, pt: XYpair) -> int:
        return self.heat_loss[pt.y][pt.x]

    def neighbors(self, pt: XYpair) -> list[tuple[XYpair, str]]:
        all_neighbors: list[tuple[XYpair, str]] = [(pt.up(), '^'),
                                                   (pt.down(), 'v'),
                                                   (pt.left(), '<'),
                                                   (pt.right(), '>')]
        return [n for n in all_neighbors if n[0] in self]

    @staticmethod
    def go_straight(pt: XYpair, direction: str) -> XYpair:
        match direction:
            case '^':
                return pt.up()
            case 'v':
                return pt.down()
            case '<':
                return pt.left()
            case '>':
                return pt.right()

    @staticmethod
    def turn_left(pt: XYpair, direction: str) -> (XYpair, str):
        match direction:
            case '^':
                return pt.left(), '<'
            case 'v':
                return pt.right(), '>'
            case '<':
                return pt.down(), 'v'
            case '>':
                return pt.up(), '^'

    @staticmethod
    def turn_right(pt: XYpair, direction: str) -> (XYpair, str):
        match direction:
            case '^':
                return pt.right(), '>'
            case 'v':
                return pt.left(), '<'
            case '<':
                return pt.up(), '^'
            case '>':
                return pt.down(), 'v'

    @functools.lru_cache(maxsize=None)
    def minimal_heat_loss(self, start: XYpair, end: XYpair, visited: tuple[XYpair, ...], direction: str = '', can_go_straight: bool = True) -> int:
        if start == end:
            return 0

        visited += start

        if not direction:
            return min(self.heat_loss_at(pt) + self.minimal_heat_loss(pt, end, (start,), in_dir) for pt, in_dir in self.neighbors(start))

        min_loss: int = self.inf

        # Go straight if on board and not 3 in a row yet
        if can_go_straight:
            straight: XYpair = self.go_straight(start, direction)
            if straight in self and straight not in visited:
                min_loss = min(min_loss, self.heat_loss_at(straight) + self.minimal_heat_loss(straight, end, visited, direction, False))

        # Go left if on board
        left: tuple[XYpair, str] = self.turn_left(start, direction)
        if left[0] in self and left[0] not in visited:
            min_loss = min(min_loss, self.heat_loss_at(left[0]) + self.minimal_heat_loss(left[0], end, visited, left[1]))

        # Go right if on board
        right: tuple[XYpair, str] = self.turn_right(start, direction)
        if right[0] in self and right[0] not in visited:
            min_loss = min(min_loss, self.heat_loss_at(right[0]) + self.minimal_heat_loss(right[0], end, visited, right[1]))

        return min_loss

    def dijkstra_heat_loss(self, start: XYpair, end: XYpair) -> int:
        prev_pos: dict[XYpair, XYpair] = {}  # defaultdict(list)
        min_heat_loss: dict[XYpair, int] = {XYpair(x, y): self.inf for y in range(self.height) for x in range(self.width)}
        min_heat_loss[start] = 0

        visited: set[XYpair] = set()
        to_check: list[tuple[int, XYpair]] = [(min_heat_loss[start], start)]
        prev_pos[start] = start
        while end not in visited:
            _, cur_pt = heapq.heappop(to_check)
            # while cur_pt in visited:
            #    _, cur_pt = heapq.heappop(to_check)

            for n in cur_pt.neighbors():
                if n in self and n not in visited and not four_in_a_row(n, cur_pt, prev_pos[cur_pt], prev_pos[prev_pos[cur_pt]]):
                    loss: int = min_heat_loss[cur_pt] + self.heat_loss_at(n)
                    if loss < min_heat_loss[n]:
                        min_heat_loss[n] = loss
                        prev_pos[n] = cur_pt
                    heapq.heappush(to_check, (min_heat_loss[n], n))
            visited.add(cur_pt)
        print(min_heat_loss[end])
        return min_heat_loss[end]


def four_in_a_row(pt1: XYpair, pt2: XYpair, pt3: XYpair, pt4: XYpair) -> bool:
    return (pt1 == pt2.up() and pt2 == pt3.up() and pt3 == pt4.up()) or \
           (pt1 == pt2.down() and pt2 == pt3.down() and pt3 == pt4.down()) or \
           (pt1 == pt2.left() and pt2 == pt3.left() and pt3 == pt4.left()) or \
           (pt1 == pt2.right() and pt2 == pt3.right() and pt3 == pt4.right())


def parse(puzzle_input):
    """Parse input"""
    return HeatLossMap([[int(block) for block in line] for line in puzzle_input.split('\n')])


def part1(data):
    """Solve part 1"""
    # return data.minimal_heat_loss(XYpair(0, 0), XYpair(data.width - 1, data.height - 1), tuple())
    return data.dijkstra_heat_loss(XYpair(0, 0), XYpair(data.width - 1, data.height - 1))


def part2(data):
    """Solve part 2"""
    return data


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = None  #part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 102
    PART2_TEST_ANSWER = None

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
