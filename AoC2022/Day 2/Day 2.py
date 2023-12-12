import pathlib
import sys
import os

scores: dict[str, int] = {'LOSE': 0,
                          'DRAW': 3,
                          'WIN': 6,
                          'R': 1,
                          'P': 2,
                          'S': 3}

beats: dict[str, str] = {'R': 'S',
                         'P': 'R',
                         'S': 'P'}
loses: dict[str, str] = {l: w for w, l in beats.items()}


def parse(puzzle_input):
    """Parse input"""
    return [tuple(line.split()) for line in puzzle_input.split('\n')]


def translate_guide_1(guide: list[tuple[str, str]]) -> list[tuple[str, str]]:
    for opp, player in guide:
        match opp:
            case 'A':
                a: str = 'R'
            case 'B':
                a: str = 'P'
            case 'C':
                a: str = 'S'
            case _:
                a: str = ''

        match player:
            case 'X':
                b: str = 'R'
            case 'Y':
                b: str = 'P'
            case 'Z':
                b: str = 'S'
            case _:
                b: str = ''

        yield a, b


def translate_guide_2(guide: list[tuple[str, str]]) -> list[tuple[str, str]]:
    for opp, player in guide:
        match opp:
            case 'A':
                a: str = 'R'
            case 'B':
                a: str = 'P'
            case 'C':
                a: str = 'S'
            case _:
                a: str = ''

        match player:
            case 'X':
                b: str = beats[a]
            case 'Y':
                b: str = a
            case 'Z':
                b: str = loses[a]
            case _:
                b: str = ''

        yield a, b


def result(opp_move: str, player_move: str) -> str:
    if opp_move == player_move:
        return 'DRAW'
    if beats[player_move] == opp_move:
        return 'WIN'
    return 'LOSE'


def round_score(opp_move: str, player_move: str) -> int:
    return scores[result(opp_move, player_move)] + scores[player_move]


def part1(data):
    """Solve part 1"""

    return sum([round_score(*r) for r in translate_guide_1(data)])


def part2(data):
    """Solve part 2"""

    return sum([round_score(*r) for r in translate_guide_2(data)])


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
