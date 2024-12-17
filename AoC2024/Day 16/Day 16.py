import functools
import pathlib
import sys
import os
from typing import Iterable

from xypair import XYpair
from pointwalker import Heading, PointWalker
from space import Space


class ReindeerMaze(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.start: XYpair = self.initial_position('S')
        self.end: XYpair = self.initial_position('E')
        self.walls: set[XYpair] = self.items['#']

        self.score: dict[XYpair, int] = {}
        self.heading: dict[XYpair, Heading] = {}
        self.paths: dict[XYpair, set[tuple[XYpair, ...]]] = {}

    def lowest_score(self) -> int:
        current: set[XYpair] = {self.start}
        new_pts: set[XYpair] = set()
        self.score = {self.start: 0}
        self.heading = {self.start: Heading.EAST}
        self.paths = {self.start: {(self.start, )}}

        while current:
            while current:
                pt: XYpair = current.pop()
                targets: set[XYpair] = pt.neighbors() - self.walls

                for target in targets:
                    cur_score: int = self.score[pt] + 1
                    move_heading: Heading = Heading.NORTH
                    if target == pt.left():
                        move_heading = Heading.WEST
                    elif target == pt.right():
                        move_heading = Heading.EAST
                    elif target == pt.down():
                        move_heading = Heading.SOUTH

                    if move_heading != self.heading[pt]:
                        cur_score += 1000

                    if target in self.score and cur_score > self.score[target]:
                        continue

                    target_paths: set[tuple[XYpair, ...]] = {path + (target,) for path in self.paths[pt]}
                    if cur_score == self.score.get(target, 0):
                        self.paths[target].update(target_paths)

                    elif target not in self.score or cur_score < self.score[target]:
                        self.score[target] = cur_score
                        self.heading[target] = move_heading
                        self.paths[target] = target_paths
                        new_pts.add(target)

            current = new_pts
            new_pts = set()

        return self.score[self.end]

    def lowest_score_path_points(self) -> set[XYpair]:
        self.lowest_score()
        path_points: set[XYpair] = set()
        for path in self.paths[self.end]:
            path_points.update(path)
            self.items['O'] = set(path)
            print(self)
            print()
            del self.items['O']
        print(len(path_points))

        return path_points

    @functools.cache
    def dfs(self, pos: XYpair, heading: Heading, visited: Iterable[XYpair] = tuple(), max_score: float = float('inf')) -> (float, set[XYpair]):
        if pos == self.end:
            return 0, {self.end}

        visited = set(visited)
        visited.add(pos)

        score: float = 0
        path: set[XYpair] = {pos}

        walker: PointWalker = PointWalker(pos, heading)
        next_steps: set[XYpair] = walker.position.neighbors() - self.walls - visited
        while len(next_steps) == 1:
            target: XYpair = next_steps.pop()
            if target == walker.peek('LEFT'):
                walker.turn('LEFT')
                score += 1000
            elif target == walker.peek('RIGHT'):
                walker.turn('RIGHT')
                score += 1000
            elif target == walker.peek('BACKWARD'):
                walker.turn('BACKWARD')
                score += 2000

            walker.step()
            path.add(walker.position)
            score += 1
            if walker.position == self.end:
                return score, path
            visited.add(walker.position)
            next_steps = walker.position.neighbors() - self.walls - visited
            if score > max_score:
                return float('inf'), set()

        if not next_steps:
            return float('inf'), set()

        lowest_score: float = float('inf')
        lowest_path: set[XYpair] = set()
        for target in next_steps:
            sub_score: float = score
            new_heading: Heading = walker.heading
            if target == walker.peek('LEFT'):
                new_heading = walker.heading.left()
                sub_score += 1000
            elif target == walker.peek('RIGHT'):
                new_heading = walker.heading.right()
                sub_score += 1000
            sub_score += 1
            if sub_score > max_score:
                continue

            new_sub_score, sub_path = self.dfs(target, new_heading, tuple(visited), lowest_score - score)
            sub_score += new_sub_score
            if sub_score < lowest_score:
                lowest_score = sub_score
                lowest_path = path | sub_path
            elif sub_score == lowest_score:
                lowest_path.update(path | sub_path)

        return lowest_score, lowest_path


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    maze: ReindeerMaze = ReindeerMaze(data)
    #return maze.lowest_score()
    return maze.dfs(maze.start, Heading.EAST)[0]


def part2(data):
    """Solve part 2"""
    maze: ReindeerMaze = ReindeerMaze(data)
    #return len(maze.lowest_score_path_points())
    return len(maze.dfs(maze.start, Heading.EAST)[1])


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    print('part 1 done')
    data = parse(puzzle_input)
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
