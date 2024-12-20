import pathlib
import sys
import os
import collections
from typing import Generator

from space import Space
from xypair import XYpair


class Racetrack(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.start: XYpair = self.initial_position('S')
        self.end: XYpair = self.initial_position('E')
        self.walls: set[XYpair] = self.items['#']
        self.cheats: dict[XYpair, set[XYpair]] = collections.defaultdict(set)

        cur_pt: XYpair = self.start
        prev_pt: XYpair = self.start
        self.track: list[XYpair] = [self.start]
        while cur_pt != self.end:
            prev_pt, cur_pt = cur_pt, (self.neighbors(cur_pt) - {prev_pt} - self.walls).pop()
            self.track.append(cur_pt)
        
        self.base_time: dict[XYpair, int] = {}
        for i, pt in enumerate(self.track):
            self.base_time[pt] = i

    def time_from_start(self, pt: XYpair) -> int:
        return self.base_time[pt]

    def time_to_end(self, pt: XYpair) -> int:
        return self.base_time[self.end] - self.base_time[pt]
    
    def iter_cheats(self) -> Generator[tuple[XYpair, XYpair], None, None]:
        for start in self.cheats:
            for finish in self.cheats[start]:
                yield start, finish

    def find_cheats(self, max_cheat_time: int = 2) -> None:
        for cheat_time in range(2, max_cheat_time + 1):
            print(f'Cheat time = {cheat_time}')
            for i, start in enumerate(self.track[:-(cheat_time + 1)]):
                for finish in self.surrounding(start, cheat_time).intersection(self.track[i + cheat_time:]):
                    if finish not in self.cheats[start] and self.time_saved(start, finish) > 0:
                        self.cheats[start].add(finish)

    def time_saved(self, start: XYpair, finish: XYpair) -> int:
        return self.base_time[finish] - self.base_time[start] - start.manhattan_distance(finish)


def parse(puzzle_input: str):
    """Parse input"""
    return puzzle_input


def part1(data):
    """Solve part 1"""
    track: Racetrack = Racetrack(data)
    track.find_cheats(2)
    return sum(track.time_saved(start, finish) >= 100 for start, finish in track.iter_cheats())


def part2(data):
    """Solve part 2"""
    track: Racetrack = Racetrack(data)
    track.find_cheats(20)
    """cheat_savings: dict[int, int] = collections.defaultdict(int)
    for start, finish in track.iter_cheats():
        savings: int = track.time_saved(start, finish)
        cheat_savings[savings] += 1
    for k, v in sorted(cheat_savings.items()):
        print(f'There are {v} cheats that save {k} picoseconds.')"""
    return sum(track.time_saved(start, finish) >= 100 for start, finish in track.iter_cheats())


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
