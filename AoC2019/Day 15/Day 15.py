import pathlib
import sys
import os
from collections import namedtuple

Point = namedtuple('Point', 'x y')

sys.path.append('..')
from intcode import IntcodeComputer


class RepairDroid:
    # Status codes
    WALL: int = 0
    MOVED: int = 1
    O2_SYSTEM: int = 2

    NORTH: int = 1
    SOUTH: int = 2
    WEST: int = 3
    EAST: int = 4

    TURN_RIGHT: dict[int, int] = {NORTH: EAST,
                                  SOUTH: WEST,
                                  WEST: NORTH,
                                  EAST: SOUTH}
    TURN_LEFT: dict[int, int] = {NORTH: WEST,
                                 SOUTH: EAST,
                                 WEST: SOUTH,
                                 EAST: NORTH}

    def __init__(self, program: list[int]) -> None:
        self.origin: Point = Point(0, 0)
        self.oxygen_system: Point = self.origin
        self.walls: set[Point] = set()
        self.surface: set[Point] = {self.origin}
        self.cur_pos: Point = self.origin
        self.cur_dir: int = self.NORTH
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program

    def reset(self) -> None:
        self.cur_pos = self.origin
        self.cur_dir: int = self.NORTH
        self.computer.initialize(self.program)

    def target_pos(self) -> Point:
        match self.cur_dir:
            case 1:
                return Point(self.cur_pos.x, self.cur_pos.y + 1)
            case 2:
                return Point(self.cur_pos.x, self.cur_pos.y - 1)
            case 3:
                return Point(self.cur_pos.x - 1, self.cur_pos.y)
            case 4:
                return Point(self.cur_pos.x + 1, self.cur_pos.y)

    def neighbors(self, pt: Point) -> set[Point]:
        return {Point(pt.x, pt.y + 1),
                Point(pt.x, pt.y - 1),
                Point(pt.x - 1, pt.y),
                Point(pt.x + 1, pt.y)} & self.surface

    def move(self) -> int:
        self.computer.run([self.cur_dir])
        return self.computer.output[0]

    def turn_left(self) -> None:
        self.cur_dir = self.TURN_LEFT[self.cur_dir]

    def turn_right(self) -> None:
        self.cur_dir = self.TURN_RIGHT[self.cur_dir]

    def map_area(self) -> None:
        # Right hand on wall
        self.reset()
        status: int = -1
        found_oxygen_system: bool = False
        while status != self.O2_SYSTEM or found_oxygen_system:
            found_oxygen_system = self.oxygen_system != self.origin
            dst: Point = self.target_pos()
            status = self.move()
            if status == self.WALL:
                self.walls.add(dst)
                self.turn_left()
            else:
                self.cur_pos = dst
                self.surface.add(self.cur_pos)
                self.turn_right()
                if status == self.O2_SYSTEM:
                    self.oxygen_system = self.cur_pos

        # Left hand on wall
        self.reset()
        status = -1
        while status != self.O2_SYSTEM:
            dst = self.target_pos()
            status = self.move()
            if status == self.WALL:
                self.walls.add(dst)
                self.turn_right()
            else:
                self.cur_pos = dst
                self.surface.add(self.cur_pos)
                self.turn_left()

    def shortest_path_len(self, start: Point, end: Point) -> int:
        num_steps: int = 0
        checked: set[Point] = set()
        to_check: set[Point] = {start}

        while end not in to_check:
            num_steps += 1
            new_to_check: set[Point] = set()
            for pt in to_check:
                new_to_check |= self.neighbors(pt)

            checked |= to_check
            to_check = new_to_check - checked

        return num_steps

    def fill_with_oxygen(self) -> int:
        num_steps: int = 0
        checked: set[Point] = set()
        to_check: set[Point] = {self.oxygen_system}

        while (checked | to_check) != self.surface:
            num_steps += 1
            new_to_check: set[Point] = set()
            for pt in to_check:
                new_to_check |= self.neighbors(pt)

            checked |= to_check
            to_check = new_to_check - checked

        return num_steps


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    droid: RepairDroid = RepairDroid(data)
    droid.map_area()
    return droid.shortest_path_len(droid.origin, droid.oxygen_system)


def part2(data):
    """Solve part 2"""
    droid: RepairDroid = RepairDroid(data)
    droid.map_area()
    return droid.fill_with_oxygen()


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
