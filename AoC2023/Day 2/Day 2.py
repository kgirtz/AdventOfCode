import pathlib
import sys
import os
import dataclasses


class Handful:
    def __init__(self, counts: str = '') -> None:
        self.cubes: dict[str, int] = {}

        if counts:
            for cubes in counts.split(','):
                color: str = cubes.strip().split()[1]
                number: int = int(cubes.strip().split()[0])
                self.cubes[color] = number

    def __le__(self, other: 'Handful') -> bool:
        return all(self.cubes[color] <= other.cubes[color] for color in self.cubes)

    def power(self) -> int:
        p: int = 1
        for number in self.cubes.values():
            p *= number
        return p


@dataclasses.dataclass
class Game:
    id: int = 0
    rounds: list[Handful] = dataclasses.field(default_factory=list)

    def cube_colors(self) -> list[str]:
        colors: set[str] = set()
        for rd in self.rounds:
            colors |= rd.cubes.keys()
        return list(colors)


def parse(puzzle_input):
    """Parse input"""
    games: list[Game] = []
    for line in puzzle_input.split('\n'):
        title, rounds = line.split(':')
        game_id: int = int(title.split()[1])
        handfuls: list[Handful] = [Handful(rd.strip()) for rd in rounds.split(';')]
        games.append(Game(game_id, handfuls))
    return games


def part1(data):
    """Solve part 1"""
    max_cubes: Handful = Handful('12 red, 13 green, 14 blue')

    possible_games: list[Game] = [game for game in data if all(rd <= max_cubes for rd in game.rounds)]

    return sum(game.id for game in possible_games)


def part2(data):
    """Solve part 2"""
    total_power: int = 0
    for game in data:
        fewest: Handful = Handful()
        for color in game.cube_colors():
            fewest.cubes[color] = max(rd.cubes.get(color, 0) for rd in game.rounds)

        total_power += fewest.power()

    return total_power


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 8
    PART2_TEST_ANSWER = 2286

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
