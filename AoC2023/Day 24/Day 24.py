import pathlib
import sys
import os
from cube import Cube
from typing import Optional, Iterable


class Hailstone:
    def __init__(self, position: Cube, velocity: Cube) -> None:
        self.position: Cube = position
        self.velocity: Cube = velocity

    def at_time(self, t: int) -> tuple[float, float, float]:
        x: float = self.velocity.x * t + self.position.x
        y: float = self.velocity.y * t + self.position.y
        z: float = self.velocity.z * t + self.position.z
        return x, y, z


def parse(puzzle_input):
    """Parse input"""
    hailstones: list[Hailstone] = []
    for line in puzzle_input.split('\n'):
        position_str, velocity_str = line.split(' @ ')
        position: Cube = Cube(*(int(component) for component in position_str.split(',')))
        velocity: Cube = Cube(*(int(component) for component in velocity_str.split(',')))
        hailstones.append(Hailstone(position, velocity))
    return hailstones


def will_intersect_at(stone1: Hailstone, stone2: Hailstone, include_z: bool = False) -> Optional[tuple[float, float, float]]:
    slope1: float = stone1.velocity.y / stone1.velocity.x
    slope2: float = stone2.velocity.y / stone2.velocity.x

    if slope1 == slope2:
        return None

    x: float = (slope2 * stone2.position.x - slope1 * stone1.position.x + stone1.position.y - stone2.position.y) / (slope2 - slope1)
    y: float = slope1 * (x - stone1.position.x) + stone1.position.y

    if (x - stone1.position.x) / stone1.velocity.x < 0 or (x - stone2.position.x) / stone2.velocity.x < 0:
        return None

    if not include_z:
        return round(x, 3), round(y, 3), 0.0

    slope1 = stone1.velocity.z / stone1.velocity.x
    slope2 = stone2.velocity.z / stone2.velocity.x
    z: float = slope1 * (x - stone1.position.x) + stone1.position.z

    if z == slope2 * (x - stone2.position.x) + stone2.position.z:
        return x, y, z
    else:
        return None


def intersect_all(hailstones: Iterable[Hailstone]) -> Hailstone:


    return Hailstone(Cube(0, 0, 0), Cube(0, 0, 0))


def part1(data):
    """Solve part 1"""
    area_min: int = 200000000000000  # test = 7, input = 200000000000000
    area_max: int = 400000000000000  # test = 27, input = 400000000000000

    intersections_in_area: int = 0
    for i, stone1 in enumerate(data[:-1]):
        for stone2 in data[i + 1:]:
            pt: Optional[tuple[float, float, float]] = will_intersect_at(stone1, stone2)
            if pt is not None and area_min <= pt[0] <= area_max and area_min <= pt[1] <= area_max:
                intersections_in_area += 1

    return intersections_in_area


def part2(data):
    """Solve part 2"""
    rock: Hailstone = intersect_all(data)
    return sum(rock.position)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = None  # test = 2, input = None
    PART2_TEST_ANSWER = 47

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
