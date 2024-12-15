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
                pt: XYpair = self.robot
                boxes: set[XYpair] = set()
                while pt.up() not in self.walls:
                    pt = pt.up()
                    if pt in self.boxes:
                        boxes.add(pt)

                if empty_spaces := self.robot.manhattan_distance(pt) - len(boxes):
                    self.robot = self.robot.up(empty_spaces)
                    self.boxes -= boxes
                    self.boxes |= {XYpair(pt.x, y) for y in range(pt.y, self.robot.y)}

            case 'v':
                pt: XYpair = self.robot
                boxes: set[XYpair] = set()
                while pt.down() not in self.walls:
                    pt = pt.down()
                    if pt in self.boxes:
                        boxes.add(pt)

                if empty_spaces := self.robot.manhattan_distance(pt) - len(boxes):
                    self.robot = self.robot.down(empty_spaces)
                    self.boxes -= boxes
                    self.boxes |= {XYpair(pt.x, y) for y in range(pt.y, self.robot.y, -1)}

            case '>':
                pt: XYpair = self.robot
                boxes: set[XYpair] = set()
                while pt.right() not in self.walls:
                    pt = pt.right()
                    if pt in self.boxes:
                        boxes.add(pt)

                if empty_spaces := self.robot.manhattan_distance(pt) - len(boxes):
                    self.robot = self.robot.right(empty_spaces)
                    self.boxes -= boxes
                    self.boxes |= {XYpair(x, pt.y) for x in range(pt.x, self.robot.x, -1)}

            case '<':
                pt: XYpair = self.robot
                boxes: set[XYpair] = set()
                while pt.left() not in self.walls:
                    pt = pt.left()
                    if pt in self.boxes:
                        boxes.add(pt)

                if empty_spaces := self.robot.manhattan_distance(pt) - len(boxes):
                    self.robot = self.robot.left(empty_spaces)
                    self.boxes -= boxes
                    self.boxes |= {XYpair(x, pt.y) for x in range(pt.x, self.robot.x)}


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
    return data


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
