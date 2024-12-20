import pathlib
import sys
import os

from xypair import XYpair
from pointwalker import State, Heading, PointWalker
from space import Space


class ReindeerMaze(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.start: XYpair = self.initial_position('S')
        self.end: XYpair = self.initial_position('E')
        self.walls: set[XYpair] = self.items['#']

        self.score: dict[State, int] = {}
        self.paths: dict[State, set[tuple[State, ...]]] = {}
        self.lowest_path_score: int = 0
        self.lowest_path_points: set[XYpair] = set()

        self.analyze()

    def analyze(self) -> None:
        init_state: State = State(self.start, Heading.EAST)
        current: set[State] = {init_state}
        new_pts: set[State] = set()
        self.score = {init_state: 0}
        self.paths = {init_state: {(init_state, )}}

        while current:
            while current:
                cur_state: State = current.pop()
                if cur_state.position == self.end:
                    continue

                targets: set[tuple[State, int]] = set()
                forward: PointWalker = PointWalker(cur_state.position, cur_state.heading)
                if forward.next() not in self.walls:
                    targets.add((State(forward.next(), cur_state.heading), self.score[cur_state] + 1))
                if forward.peek('LEFT') not in self.walls:
                    targets.add((State(cur_state.position, cur_state.heading.left()), self.score[cur_state] + 1000))
                if forward.peek('RIGHT') not in self.walls:
                    targets.add((State(cur_state.position, cur_state.heading.right()), self.score[cur_state] + 1000))

                for next_state, next_score in targets:
                    if next_state not in self.score or next_score <= self.score[next_state]:
                        target_paths: set[tuple[State, ...]] = {path + (next_state,) for path in self.paths[cur_state]}
                        if next_score == self.score.get(next_state, 0):
                            self.paths[next_state].update(target_paths)  # noqa
                        else:
                            self.paths[next_state] = target_paths
                        self.score[next_state] = next_score
                        new_pts.add(next_state)

            current = new_pts
            new_pts = set()

        # Aggregate path points
        self.lowest_path_points = set()
        min_score: int = self.min_score(self.end)
        for s, paths in self.paths.items():
            if s.position == self.end and self.score[s] == min_score:
                for path in paths:
                    self.lowest_path_points.update(s.position for s in path)

        self.lowest_path_score = self.min_score(self.end)

    def min_score(self, pt: XYpair) -> int:
        return min(self.score[state] for state in self.score if state.position == pt)


def parse(puzzle_input: str):
    """Parse input"""
    return ReindeerMaze(puzzle_input)


def part1(maze):
    """Solve part 1"""
    return maze.lowest_path_score


def part2(maze):
    """Solve part 2"""
    return len(maze.lowest_path_points)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 11048
    PART2_TEST_ANSWER = 64

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
