import pathlib
import sys
import os
from typing import Sequence
from point import Point


class Platform:
    def __init__(self, platform: Sequence[str]) -> None:
        self.height: int = len(platform)
        self.width: int = len(platform[0])
        self.round_rocks: list[Point] = []
        self.cube_rocks: list[Point] = []

        for y, line in enumerate(platform):
            for x, pt in enumerate(line):
                match pt:
                    case 'O':
                        self.round_rocks.append(Point(x, y))
                    case '#':
                        self.cube_rocks.append(Point(x, y))

    def tilt_north(self) -> None:
        rocks_to_move: list[Point] = sorted(self.round_rocks, key=lambda pt: pt.y)
        resting_rocks: set[Point] = set(self.cube_rocks)
        self.round_rocks = []
        for rock in rocks_to_move:
            y: int = rock.y
            while y > 0 and Point(rock.x, y - 1) not in resting_rocks:
                y -= 1
            self.round_rocks.append(Point(rock.x, y))
            resting_rocks.add(Point(rock.x, y))

    def tilt_south(self) -> None:
        rocks_to_move: list[Point] = sorted(self.round_rocks, key=lambda pt: pt.y, reverse=True)
        resting_rocks: set[Point] = set(self.cube_rocks)
        self.round_rocks = []
        for rock in rocks_to_move:
            y: int = rock.y
            while y < self.height - 1 and Point(rock.x, y + 1) not in resting_rocks:
                y += 1
            self.round_rocks.append(Point(rock.x, y))
            resting_rocks.add(Point(rock.x, y))

    def tilt_west(self) -> None:
        rocks_to_move: list[Point] = sorted(self.round_rocks)
        resting_rocks: set[Point] = set(self.cube_rocks)
        self.round_rocks = []
        for rock in rocks_to_move:
            x: int = rock.x
            while x > 0 and Point(x - 1, rock.y) not in resting_rocks:
                x -= 1
            self.round_rocks.append(Point(x, rock.y))
            resting_rocks.add(Point(x, rock.y))

    def tilt_east(self) -> None:
        rocks_to_move: list[Point] = sorted(self.round_rocks, reverse=True)
        resting_rocks: set[Point] = set(self.cube_rocks)
        self.round_rocks = []
        for rock in rocks_to_move:
            x: int = rock.x
            while x < self.width - 1 and Point(x + 1, rock.y) not in resting_rocks:
                x += 1
            self.round_rocks.append(Point(x, rock.y))
            resting_rocks.add(Point(x, rock.y))

    def find_repeat_state(self) -> (int, int):
        seen_states: dict[tuple[Point, ...], int] = {tuple(self.round_rocks): 0}
        i: int = 0
        while True:
            i += 1
            self.cycle()

            state: tuple[Point, ...] = tuple(self.round_rocks)
            if state in seen_states:
                setup_length: int = seen_states[state]
                cycle_length: int = i - setup_length
                return setup_length, cycle_length

            seen_states[state] = i

    def cycle(self, num_cycles: int = 1) -> None:
        for i in range(num_cycles):
            self.tilt_north()
            self.tilt_west()
            self.tilt_south()
            self.tilt_east()

    def load(self, rock: Point) -> int:
        if rock not in self.round_rocks:
            return 0
        return self.height - rock.y


def parse(puzzle_input):
    """Parse input"""
    return Platform(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    data.tilt_north()
    return sum(data.load(rock) for rock in data.round_rocks)


def part2(data):
    """Solve part 2"""
    total_cycles: int = 1000000000

    setup, cycle = data.find_repeat_state()
    data.cycle(setup + (total_cycles - setup) % cycle)
    print(sum(data.load(rock) for rock in data.round_rocks))
    return sum(data.load(rock) for rock in data.round_rocks)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 136
    PART2_TEST_ANSWER = 64

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
