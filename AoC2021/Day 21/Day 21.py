import pathlib
import sys
import os
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    return [int(line.split()[-1]) for line in puzzle_input.split('\n')]


class Die:
    def __init__(self, sides) -> None:
        self.sides: int = sides
        self.num_rolls: int = 0

    def roll(self) -> int:
        result: int = self.num_rolls % self.sides + 1
        self.num_rolls += 1
        return result


def turn(cur_player: int, p1_pos: int, p1_score: int, p2_pos: int, p2_score: int, die: Die) -> tuple:
    movement: int = die.roll() + die.roll() + die.roll()
    if cur_player == 1:
        p1_pos = (p1_pos + movement - 1) % 10 + 1
        return 2, p1_pos, p1_score + p1_pos, p2_pos, p2_score

    else:
        p2_pos = (p2_pos + movement - 1) % 10 + 1
        return 1, p1_pos, p1_score, p2_pos, p2_score + p2_pos


def quantum_turn(cur_player: int, p1_pos: int, p1_score: int, p2_pos: int, p2_score: int) -> dict[tuple, int]:
    states: defaultdict[tuple, int] = defaultdict(int)
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                if cur_player == 1:
                    new_p1_pos = (p1_pos + i + j + k - 1) % 10 + 1
                    states[(2, new_p1_pos, p1_score + new_p1_pos, p2_pos, p2_score)] += 1
                else:
                    new_p2_pos = (p2_pos + i + j + k - 1) % 10 + 1
                    states[(1, p1_pos, p1_score, new_p2_pos, p2_score + new_p2_pos)] += 1
    return dict(states)


def part1(data):
    """Solve part 1"""
    cur_player: int = 1
    p1_pos, p2_pos = data
    p1_score, p2_score = 0, 0
    d100: Die = Die(100)
    while True:
        cur_player, p1_pos, p1_score, p2_pos, p2_score = turn(cur_player, p1_pos, p1_score, p2_pos, p2_score, d100)
        if p1_score >= 1000:
            return p2_score * d100.num_rolls
        if p2_score >= 1000:
            return p1_score * d100.num_rolls


def part2(data):
    """Solve part 2"""
    cur_player: int = 1
    p1_pos, p2_pos = data
    p1_score, p2_score = 0, 0

    wins: dict[int, int] = {1: 0, 2: 0}
    multiverse: defaultdict[tuple, int] = defaultdict(int)
    multiverse[(cur_player, p1_pos, p1_score, p2_pos, p2_score)] = 1

    while multiverse:
        for universe in list(multiverse.keys()):
            universe_count: int = multiverse[universe]
            del multiverse[universe]

            new_states: dict[tuple, int] = quantum_turn(*universe)
            for state in list(new_states.keys()):
                _, _, p1_score, _, p2_score = state
                if p1_score >= 21:
                    wins[1] += new_states[state] * universe_count
                elif p2_score >= 21:
                    wins[2] += new_states[state] * universe_count
                else:
                    multiverse[state] += new_states[state] * universe_count
    return max(wins.values())


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
