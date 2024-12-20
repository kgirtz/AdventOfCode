import pathlib
import sys
import os
from typing import Generator

from space import Space
from xypair import XYpair


class Racetrack(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.start: XYpair = self.initial_position('S')
        self.end: XYpair = self.initial_position('E')
        self.walls: set[XYpair] = self.items['#']
        self.base_time: dict[XYpair, int] = {self.start: 0}

        cur_pt: XYpair = self.start
        prev_pt: XYpair = self.start
        distance: int = 0
        while cur_pt != self.end:
            prev_pt, cur_pt = cur_pt, tuple(self.neighbors(cur_pt) - {prev_pt} - self.walls)[0]
            distance += 1
            self.base_time[cur_pt] = distance

    def time_from_start(self, pt: XYpair) -> int:
        return self.base_time[pt]

    def time_to_end(self, pt: XYpair) -> int:
        return self.base_time[self.end] - self.base_time[pt]

    def cheats(self, length: int) -> Generator[tuple[XYpair, XYpair], None, None]:
        for wall in self.walls:
            adjacent_tracks: set[XYpair] = self.neighbors(wall) - self.walls
            if len(adjacent_tracks) >= 2:
                earliest_step_time: int = max(self.time_to_end(t) for t in adjacent_tracks)
                for track in adjacent_tracks:
                    if self.time_to_end(track) != earliest_step_time:
                        yield wall, track

    def time_saved(self, cheat: tuple[XYpair, XYpair]) -> int:
        wall, track = cheat
        adjacent_tracks: set[XYpair] = self.neighbors(wall) - self.walls
        start_time: int = min(self.time_from_start(t) for t in adjacent_tracks)
        end_time: int = self.time_from_start(track)
        return end_time - start_time - 2

    """def base_time(self) -> int:
        current: set[XYpair] = {self.start}
        distance: dict[XYpair, int] = {self.start: 0}
        while current:
            pt: XYpair = current.pop()
            targets: set[XYpair] = self.neighbors(pt) - self.corrupted - distance.keys() - current
            current.update(targets)
            for target in targets:
                distance[target] = distance[pt] + 1
        return distance.get(self.exit, -1)"""


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""  # 1461 is too high
    track: Racetrack = Racetrack(data)
    return sum(track.time_saved(cheat) >= 100 for cheat in track.cheats(2))


def part2(data):
    """Solve part 2"""
    track: Racetrack = Racetrack(data)
    """cheat_savings: dict[int, int] = {}
        for cheat in track.cheats():
            savings: int = track.time_saved(cheat)
            if savings not in cheat_savings:
                cheat_savings[savings] = 0
            cheat_savings[savings] += 1
        for k, v in sorted(cheat_savings.items()):
            print(f'There are {v} cheats that save {k} picoseconds.')"""
    return sum(track.time_saved(cheat) >= 100 for cheat in track.cheats(20))


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 0
    PART2_TEST_ANSWER = 0

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
