import pathlib
import sys
import os

from xypair import XYpair, ORIGIN
from space import Space


class MemorySpace(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.corrupted: set[XYpair] = set()

    def shortest_path(self) -> int:
        current: set[XYpair] = {ORIGIN}
        new_pts: set[XYpair] = set()
        distance: dict[XYpair, int] = {ORIGIN: 0}
        # paths: dict[XYpair, set[tuple[XYpair, ...]]] = {ORIGIN: {(ORIGIN,)}}

        while current:
            while current:
                pt: XYpair = current.pop()
                targets: set[XYpair] = self.neighbors(pt) - self.corrupted

                for target in targets:
                    cur_score: int = distance[pt] + 1

                    if target in distance and cur_score > distance[target]:
                        continue

                    # target_paths: set[tuple[XYpair, ...]] = {path + (target,) for path in paths[pt]}
                    # if cur_score == distance.get(target, 0):
                    #    paths[target].update(target_paths)

                    elif target not in distance or cur_score < distance[target]:
                        distance[target] = cur_score
                        # paths[target] = target_paths
                        new_pts.add(target)

            current = new_pts
            new_pts = set()

        exit_pt: XYpair = XYpair(self.width - 1, self.height - 1)
        return distance.get(exit_pt, -1)

    def path_exists(self) -> int:
        exit_pt: XYpair = XYpair(self.width - 1, self.height - 1)

        finished_start: set[XYpair] = set()
        finished_end: set[XYpair] = set()
        current_start: set[XYpair] = {ORIGIN}
        current_end: set[XYpair] = {exit_pt}

        while current_start and current_end:
            start_pt: XYpair = current_start.pop()
            finished_start.add(start_pt)
            targets: set[XYpair] = self.neighbors(start_pt) - self.corrupted - finished_start
            current_start.update(targets)

            end_pt: XYpair = current_end.pop()
            finished_end.add(end_pt)
            targets = self.neighbors(end_pt) - self.corrupted - finished_end
            current_end.update(targets)

            if (finished_start | current_start) & (finished_end | current_end):
                return True

        return False


def parse(puzzle_input: str):
    """Parse input"""
    return [XYpair(*(int(n) for n in line.split(','))) for line in puzzle_input.split('\n')]


def part1(data):
    """Solve part 1"""
    side_length: int = 71  # test = 7, input = 71
    num_fallen: int = 1024  # test = 12, input = 1024

    space: MemorySpace = MemorySpace(['.' * side_length for _ in range(side_length)])
    space.corrupted = set(data[:num_fallen])
    return space.shortest_path()


def part2(data):
    """Solve part 2"""
    side_length: int = 71  # test = 7, input = 71
    num_fallen: int = 1024  # test = 12, input = 1024

    space: MemorySpace = MemorySpace(['.' * side_length for _ in range(side_length)])
    space.corrupted = set(data[:num_fallen + 1])
    while space.path_exists():
        while data[num_fallen] in space.corrupted:
            num_fallen += 1
        space.corrupted.add(data[num_fallen])
    return ','.join(str(n) for n in data[num_fallen])


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # 22
    PART2_TEST_ANSWER = None  # '6,1'

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
