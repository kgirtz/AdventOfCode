import pathlib
import sys
import os

from xypair import XYpair
from pointwalker import PointWalker, Heading
from space import Space


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

    def move_object(self, cur_pos: XYpair, heading: Heading) -> None:
        new_pos: XYpair = PointWalker(cur_pos, heading).next()
        if new_pos in self.walls:
            return
        if new_pos in self.boxes:
            if self.wide:
                self.move_wide_box(new_pos, heading)
            else:
                self.move_object(new_pos, heading)
            if new_pos in self.boxes:
                return

        if cur_pos == self.robot:
            self.robot = new_pos
        elif cur_pos in self.boxes:
            self.boxes.remove(cur_pos)
            self.boxes.add(new_pos)

    def wide_box_can_move(self, cur_pos: XYpair, heading: Heading) -> bool:
        # Default box position is left
        if cur_pos in self.right_boxes:
            cur_pos = cur_pos.left()

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
            return self.wide_box_can_move(new_pos, heading)

        # Vertical with misaligned box(es) in the way
        blocking: set[XYpair] = self.boxes & {new_pos, new_pos.right()}
        return all(self.wide_box_can_move(box, heading) for box in blocking)

    def move_wide_box(self, cur_pos: XYpair, heading: Heading) -> None:
        # Default box position is left
        if cur_pos in self.right_boxes:
            cur_pos = cur_pos.left()
        if heading == Heading.WEST:
            cur_pos = cur_pos.right()

        if heading.horizontal():
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=2)
        else:
            new_pos: XYpair = PointWalker(cur_pos, heading).peek(distance=1)

        if new_pos in self.walls or (heading.vertical() and new_pos.right() in self.walls):
            return
        if new_pos in self.boxes and not self.wide_box_can_move(new_pos, heading):
            return
        if heading.vertical() and new_pos.right() in self.left_boxes and not self.wide_box_can_move(new_pos.right(), heading):
            return

        if new_pos in self.boxes:
            self.move_wide_box(new_pos, heading)
        if heading.vertical() and new_pos.right() in self.left_boxes:
            self.move_wide_box(new_pos.right(), heading)

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

    def move_robot(self, heading: Heading) -> None:
        self.move_object(self.robot, heading)


def parse(puzzle_input: str):
    """Parse input"""
    warehouse_str, movement_str = puzzle_input.split('\n\n')
    directions: list[Heading] = [Heading.from_arrow(arrow) for arrow in movement_str.replace('\n', '')]
    return warehouse_str, directions


def part1(data):
    """Solve part 1"""
    warehouse_str, directions = data
    warehouse: Warehouse = Warehouse(warehouse_str)
    for d in directions:
        warehouse.move_robot(d)
    return sum(gps_coordinate(pt) for pt in warehouse.boxes)


def part2(data):
    """Solve part 2"""
    warehouse_str, directions = data
    warehouse: Warehouse = Warehouse(warehouse_str, wide=True)
    for d in directions:
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
