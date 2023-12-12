import pathlib
import sys
import os
from collections import namedtuple

sys.path.append('..')
from intcode import IntcodeComputer


Point = namedtuple('Point', 'x y')

WHITE = 1
BLACK = 0


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


class PaintingRobot:

    directions: list[str] = ['<', '^', '>', 'v']

    def __init__(self) -> None:
        self.computer: IntcodeComputer = IntcodeComputer()
        self.location: Point = Point(0, 0)
        self.direction: str = '^'
        self.white: set[Point] = set()
        self.panels_painted: set[Point] = set()

    def cur_color(self) -> int:
        return WHITE if self.location in self.white else BLACK

    def paint_panel(self, color: int) -> None:
        self.panels_painted.add(self.location)
        if color == WHITE:
            self.white.add(self.location)
        elif color == BLACK:
            self.white.discard(self.location)

    def rotate(self, turn: int) -> None:
        if turn == 0:
            turn = -1
        dir_i: int = (self.directions.index(self.direction) + turn) % 4
        self.direction = self.directions[dir_i]

    def move(self) -> None:
        x, y = self.location
        if self.direction == '<':
            self.location = Point(x - 1, y)
        elif self.direction == '>':
            self.location = Point(x + 1, y)
        elif self.direction == '^':
            self.location = Point(x, y + 1)
        elif self.direction == 'v':
            self.location = Point(x, y - 1)

    def paint_area(self, instructions: list[int]) -> None:
        color, turn = self.computer.execute(instructions, [self.cur_color()])

        self.paint_panel(color)
        self.rotate(turn)
        self.move()

        while self.computer.state != 'HALTED':
            color, turn = self.computer.run([self.cur_color()])

            self.paint_panel(color)
            self.rotate(turn)
            self.move()

    def print_area(self) -> None:
        x_min: int = min(panel.x for panel in self.white)
        x_max: int = max(panel.x for panel in self.white)
        y_min: int = min(panel.y for panel in self.white)
        y_max: int = max(panel.y for panel in self.white)

        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                if Point(x, y) in self.white:
                    print('#', end='')
                else:
                    print(' ', end='')
            print()


def part1(data):
    """Solve part 1"""
    robot: PaintingRobot = PaintingRobot()
    robot.paint_area(data)
    return len(robot.panels_painted)


def part2(data):
    """Solve part 2"""
    robot: PaintingRobot = PaintingRobot()
    robot.paint_panel(WHITE)
    robot.paint_area(data)
    robot.print_area()


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    part2(data)

    return solution1,


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
