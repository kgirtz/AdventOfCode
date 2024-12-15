import pathlib
import sys
import os

from xypair import XYpair
from space import Space


def gps_coordinate(pt: XYpair) -> int:
    return pt.x + 100 * pt.y


class Warehouse(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put)

        self.walls: set[XYpair] = self.items['#']
        self.boxes: set[XYpair] = self.items['O']
        self.robot: XYpair = self.initial_position('@')

    def move_robot(self, direction: str) -> None:
        match direction:
            case '^':
                if self.robot.up() in self.walls:
                    return
                if self.robot.up() not in self.boxes:
                    self.robot = self.robot.up()
                    return

                not_box: XYpair = self.robot.up(2)
                while not_box in self.boxes:
                    not_box = not_box.up()
                if not_box in self.walls:
                    return

                self.robot = self.robot.up()
                self.boxes.remove(self.robot)
                self.boxes.add(not_box)

            case 'v':
                if self.robot.down() in self.walls:
                    return
                if self.robot.down() not in self.boxes:
                    self.robot = self.robot.down()
                    return

                not_box: XYpair = self.robot.down(2)
                while not_box in self.boxes:
                    not_box = not_box.down()
                if not_box in self.walls:
                    return

                self.robot = self.robot.down()
                self.boxes.remove(self.robot)
                self.boxes.add(not_box)

            case '>':
                if self.robot.right() in self.walls:
                    return
                if self.robot.right() not in self.boxes:
                    self.robot = self.robot.right()
                    return

                not_box: XYpair = self.robot.right(2)
                while not_box in self.boxes:
                    not_box = not_box.right()
                if not_box in self.walls:
                    return

                self.robot = self.robot.right()
                self.boxes.remove(self.robot)
                self.boxes.add(not_box)

            case '<':
                if self.robot.left() in self.walls:
                    return
                if self.robot.left() not in self.boxes:
                    self.robot = self.robot.left()
                    return

                not_box: XYpair = self.robot.left(2)
                while not_box in self.boxes:
                    not_box = not_box.left()
                if not_box in self.walls:
                    return

                self.robot = self.robot.left()
                self.boxes.remove(self.robot)
                self.boxes.add(not_box)


def parse(puzzle_input: str):
    """Parse input"""
    warehouse_str, movement_str = puzzle_input.split('\n\n')
    movement_str = movement_str.replace('\n', '')
    return warehouse_str, movement_str


def part1(data):
    """Solve part 1"""
    warehouse_str, movement_str = data
    warehouse: Warehouse = Warehouse(warehouse_str)
    for d in movement_str:
        warehouse.move_robot(d)
    return sum(gps_coordinate(pt) for pt in warehouse.boxes)


def part2(data):
    """Solve part 2"""
    warehouse_str, movement_str = data
    warehouse: Warehouse = Warehouse(warehouse_str)
    for d in movement_str:
        warehouse.move_robot(d)
    return sum(gps_coordinate(pt) for pt in warehouse.boxes)


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 10092
    PART2_TEST_ANSWER = 9021

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
