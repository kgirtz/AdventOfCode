import pathlib
import sys
import os

from xypair import XYpair, accept_tuple
from pointwalker import PointWalker, Heading
from space import Space


@accept_tuple
def gps_coordinate(pt: XYpair) -> int:
    return pt.x + 100 * pt.y


def widen(warehouse: str) -> list[str]:
    big_warehouse: list[str] = []
    for line in warehouse.split('\n'):
        wide_line: str = ''
        for tile in line:
            match tile:
                case '@':
                    wide_line += '@.'
                case 'O':
                    wide_line += '[]'
                case _:
                    wide_line += 2 * tile
        big_warehouse.append(wide_line)
    return big_warehouse


class Warehouse(Space):
    def __init__(self, in_put, *, wide: bool = False) -> None:
        if wide:
            in_put = widen(in_put)

        super().__init__(in_put)

        self.walls: set[XYpair] = self.items['#']
        self.robot: XYpair = self.initial_position('@')
        self.wide: bool = wide

        if self.wide:
            self.left_boxes: set[XYpair] = self.items['[']
            self.right_boxes: set[XYpair] = self.items[']']
            self.boxes: set[XYpair] = self.left_boxes | self.right_boxes
        else:
            self.boxes: set[XYpair] = self.items['O']

    def move_object(self, cur_pos: XYpair, direction: str) -> None:
        heading: Heading = {'^': Heading.NORTH, '>': Heading.EAST, 'v': Heading.SOUTH, '<': Heading.WEST}[direction]
        new_pos: XYpair = PointWalker(cur_pos, heading).next()

        if new_pos in self.walls:
            return
        if new_pos in self.boxes:
            if self.wide:
                self.move_wide_box(new_pos, direction)
            else:
                self.move_object(new_pos, direction)
            if new_pos in self.boxes:
                return

        if cur_pos == self.robot:
            self.robot = new_pos
        elif cur_pos in self.boxes:
            self.boxes.remove(cur_pos)
            self.boxes.add(new_pos)

    def wide_box_can_move(self, cur_pos: XYpair, direction: str) -> bool:
        # Default box position is left
        if cur_pos in self.right_boxes:
            cur_pos = cur_pos.left()

        heading: Heading = {'^': Heading.NORTH, '>': Heading.EAST, 'v': Heading.SOUTH, '<': Heading.WEST}[direction]
        if heading == Heading.WEST:
            cur_pos = cur_pos.right()

        if heading.horizontal():
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=2)
        else:
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=1)

        if new_pos in self.walls or (heading.vertical() and new_pos.right() in self.walls):
            return False
        if new_pos not in self.boxes and (heading.horizontal() or new_pos.right() not in self.boxes):
            return True
        if heading.horizontal() or (heading.vertical() and new_pos in self.left_boxes):
            return self.wide_box_can_move(new_pos, direction)

        # Vertical with misaligned box(es) in the way
        blocking: set[XYpair] = self.boxes & {new_pos, new_pos.right()}
        return all(self.wide_box_can_move(box, direction) for box in blocking)

    def move_wide_box(self, cur_pos: XYpair, direction: str) -> None:
        # Default box position is left
        if cur_pos in self.right_boxes:
            cur_pos = cur_pos.left()

        heading: Heading = {'^': Heading.NORTH, '>': Heading.EAST, 'v': Heading.SOUTH, '<': Heading.WEST}[direction]
        if heading == Heading.WEST:
            cur_pos = cur_pos.right()

        if heading.horizontal():
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=2)
        else:
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=1)

        if new_pos in self.walls or (heading.vertical() and new_pos.right() in self.walls):
            return
        if new_pos in self.boxes and not self.wide_box_can_move(new_pos, direction):
            return
        if heading.vertical() and new_pos.right() in self.left_boxes and not self.wide_box_can_move(new_pos.right(), direction):
            return

        if new_pos in self.boxes:
            self.move_wide_box(new_pos, direction)
        if heading.vertical() and new_pos.right() in self.left_boxes:
            self.move_wide_box(new_pos.right(), direction)

        match heading:
            case Heading.EAST:
                self.left_boxes.remove(cur_pos)
                self.left_boxes.add(cur_pos.right())
                self.right_boxes.remove(cur_pos.right())
                self.right_boxes.add(new_pos)
            case Heading.WEST:
                self.left_boxes.remove(cur_pos.left())
                self.left_boxes.add(new_pos)
                self.right_boxes.remove(cur_pos)
                self.right_boxes.add(cur_pos.left())
            case _:
                self.left_boxes.remove(cur_pos)
                self.left_boxes.add(new_pos)
                self.right_boxes.remove(cur_pos.right())
                self.right_boxes.add(new_pos.right())

        self.boxes = self.left_boxes | self.right_boxes

    def move_robot(self, direction: str) -> None:
        self.move_object(self.robot, direction)

    def move_robot_wide(self, direction: str) -> None:
        match direction:
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
                self.left_boxes -= {(x, self.robot.y) for x in range(self.robot.x, not_box.x, 2)}
                self.left_boxes |= {(x, self.robot.y) for x in range(self.robot.x + 1, not_box.x, 2)}
                self.right_boxes -= {(x, self.robot.y) for x in range(self.robot.x + 1, not_box.x, 2)}
                self.right_boxes |= {(x, self.robot.y) for x in range(self.robot.x + 2, not_box.x + 1, 2)}

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
                self.right_boxes -= {(x, self.robot.y) for x in range(self.robot.x, not_box.x, -2)}
                self.right_boxes |= {(x, self.robot.y) for x in range(self.robot.x - 1, not_box.x, -2)}
                self.left_boxes -= {(x, self.robot.y) for x in range(self.robot.x - 1, not_box.x, -2)}
                self.left_boxes |= {(x, self.robot.y) for x in range(self.robot.x - 2, not_box.x - 1, -2)}


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
    warehouse: Warehouse = Warehouse(warehouse_str, wide=True)
    for d in movement_str:
        warehouse.move_robot(d)
    return sum(gps_coordinate(pt) for pt in warehouse.left_boxes)


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
