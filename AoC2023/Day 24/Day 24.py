import pathlib
import sys
import os
from cube import Cube
from typing import Optional, Sequence


class Hailstone:
    def __init__(self, position: Cube, velocity: Cube) -> None:
        self.initial_position: Cube = position
        self.velocity: Cube = velocity

    def position(self, *, t: int) -> Cube:
        x: int = self.velocity.x * t + self.initial_position.x
        y: int = self.velocity.y * t + self.initial_position.y
        z: int = self.velocity.z * t + self.initial_position.z
        return Cube(x, y, z)

    def time(self, x: int) -> int:
        return (x - self.initial_position.x) // self.velocity.x

    def path_intersection(self, other: 'Hailstone', ignore_z: bool = False) -> Optional[tuple[float, float, float]]:
        self_slope_xy: float = self.velocity.y / self.velocity.x
        other_slope_xy: float = other.velocity.y / other.velocity.x

        if self_slope_xy == other_slope_xy:
            return None

        x: float = (other_slope_xy * other.initial_position.x
                    - self_slope_xy * self.initial_position.x
                    + self.initial_position.y
                    - other.initial_position.y) / (other_slope_xy - self_slope_xy)
        y: float = self_slope_xy * (x - self.initial_position.x) + self.initial_position.y

        if self.time(round(x)) <= 0 or other.time(round(x)) <= 0:
            return None

        if ignore_z:
            return round(x, 3), round(y, 3), 0.0

        self_slope_xz: float = self.velocity.z / self.velocity.x
        other_slope_xz: float = other.velocity.z / other.velocity.x
        self_z: float = self_slope_xz * (x - self.initial_position.x) + self.initial_position.z
        other_z: float = other_slope_xz * (x - other.initial_position.x) + other.initial_position.z

        if self_z == other_z:
            return round(x, 3), round(y, 3), round(self_z, 3)

        return None

    def will_hit(self, other: 'Hailstone') -> bool:
        intersection_point: Optional[tuple[float, float, float]] = self.path_intersection(other)
        if intersection_point is None:
            return False
        rounded: Cube = Cube(*(round(c) for c in intersection_point))
        if rounded != intersection_point:
            return False
        return self.time(rounded.x) == other.time(rounded.x)


def parse(puzzle_input):
    """Parse input"""
    hailstones: list[Hailstone] = []
    for line in puzzle_input.split('\n'):
        position_str, velocity_str = line.split(' @ ')
        position: Cube = Cube(*(int(component) for component in position_str.split(',')))
        velocity: Cube = Cube(*(int(component) for component in velocity_str.split(',')))
        hailstones.append(Hailstone(position, velocity))
    return hailstones


def hits_all_stones(rock: Hailstone, hailstones: Sequence[Hailstone]) -> bool:
    # "Rewind" so we don't intersect in the past
    rock.initial_position = rock.position(t=-100000000000000)

    # Do we intersect every other line in the future?
    if any(rock.path_intersection(stone) is None for stone in hailstones):
        return False

    # Shift starting position to make line intersections actual hits
    intersection_x, _, _ = rock.path_intersection(hailstones[0])
    origin_time: int = rock.time(round(intersection_x)) - hailstones[0].time(round(intersection_x))
    rock.initial_position = rock.position(t=origin_time)

    # Do we hit every hailstone?
    return all(rock.will_hit(stone) for stone in hailstones)


def intersect_all(hailstones: Sequence[Hailstone]) -> Hailstone:
    min_distance: int = 10000000000000000000
    close: list[Hailstone] = []
    for i, h1 in enumerate(hailstones[:-1]):
        for h2 in hailstones[i + 1:]:
            distance: int = h1.initial_position.manhattan_distance(h2.initial_position)
            if distance < min_distance:
                min_distance = distance
                close = [h1, h2]

    # Determine correct line then time
    for t0 in range(1, 1000):
        initial_positions: tuple[Cube, Cube] = (close[0].position(t=t0), close[1].position(t=t0))
        for dt in range(1000000, 1001000):
            final_positions: tuple[Cube, Cube] = (close[1].position(t=t0 + dt), close[0].position(t=t0 + dt))

            for initial_position, final_position in zip(initial_positions, final_positions):
                if (final_position.x - initial_position.x) % dt != 0 or \
                   (final_position.y - initial_position.y) % dt != 0 or \
                   (final_position.z - initial_position.z) % dt != 0:
                    continue

                vel_x: int = (final_position.x - initial_position.x) // dt
                vel_y: int = (final_position.y - initial_position.y) // dt
                vel_z: int = (final_position.z - initial_position.z) // dt
                intersector: Hailstone = Hailstone(initial_position, Cube(vel_x, vel_y, vel_z))

                if hits_all_stones(intersector, hailstones):
                    return intersector

    return Hailstone(Cube(0, 0, 0), Cube(1, 1, 1))


def part1(data):
    """Solve part 1"""
    area_min: int = 200000000000000  # test = 7, input = 200000000000000
    area_max: int = 400000000000000  # test = 27, input = 400000000000000

    intersections_in_area: int = 0
    for i, stone1 in enumerate(data[:-1]):
        for stone2 in data[i + 1:]:
            pt: Optional[tuple[float, float, float]] = stone1.path_intersection(stone2, ignore_z=True)
            if pt is not None and area_min <= pt[0] <= area_max and area_min <= pt[1] <= area_max:
                intersections_in_area += 1

    return intersections_in_area


def part2(data):
    """Solve part 2"""
    rock: Hailstone = intersect_all(data)
    return sum(rock.initial_position)


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
    PART2_TEST_ANSWER = None # 47

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