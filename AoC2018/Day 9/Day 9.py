import pathlib
import sys
import os
from typing import Self


def parse(puzzle_input: str):
    """Parse input"""
    words: list[str] = puzzle_input.split()
    return int(words[0]), int(words[6])


class Marble:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.clockwise: Marble = self
        self.counter: Marble = self

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'

    def place_after(self, new_marble: Self) -> None:
        new_marble.clockwise = self.clockwise
        new_marble.counter = self
        new_marble.clockwise.counter = new_marble
        new_marble.counter.clockwise = new_marble

    def remove(self) -> None:
        self.clockwise.counter = self.counter
        self.counter.clockwise = self.clockwise

    def move_counter(self, steps: int = 1) -> Self:
        m: Marble = self
        for _ in range(steps):
            m = m.counter
        return m


def take_turn(current_marble: Marble, next_marble: int) -> (Marble, int):
    if next_marble % 23 == 0:
        removed: Marble = current_marble.move_counter(7)
        new_current: Marble = removed.clockwise
        removed.remove()

        score: int = next_marble + removed.value
        return new_current, score

    new_marble: Marble = Marble(next_marble)
    current_marble.clockwise.place_after(new_marble)
    return new_marble, 0


def winner(num_players: int, last_marble: int) -> int:
    scores: list[int] = [0] * num_players

    # First turn - trivial
    current_marble: Marble = Marble(0)

    # Remaining turns
    for next_marble in range(1, last_marble + 1):
        current_marble, points_earned = take_turn(current_marble, next_marble)
        player: int = next_marble % num_players
        scores[player] += points_earned
    return max(scores)


def part1(data):
    """Solve part 1"""
    num_players, last_marble = data
    return winner(num_players, last_marble)


def part2(data):
    """Solve part 2"""
    num_players, last_marble = data
    return winner(num_players, last_marble * 100)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 32
    PART2_TEST_ANSWER = None

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
