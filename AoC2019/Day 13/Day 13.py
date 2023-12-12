import pathlib
import sys
import os
from collections import namedtuple

sys.path.append('..')
from intcode import IntcodeComputer

Tile = namedtuple('Tile', 'x y')


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


class BrickGame:
    def __init__(self, program: list[int]) -> None:
        self.walls: set[Tile] = set()
        self.blocks: set[Tile] = set()
        self.paddle: Tile = Tile(0, 0)
        self.ball: Tile = Tile(0, 0)
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program
        self.score: int = 0
        self.result: str = ''
        self.left_wall: int = 1
        self.right_wall: int = 0
        self.top_wall: int = 1

    def __str__(self) -> str:
        x_max: int = max(t.x for t in self.walls)
        y_max: int = max(t.y for t in self.walls)

        display: dict[Tile, str] = {block: '=' for block in self.blocks}
        for wall in self.walls:
            display[wall] = '#'
        display[self.paddle] = '='
        display[self.ball] = 'O'

        display_str: str = ''
        for y in range(y_max + 1):
            for x in range(x_max + 1):
                display_str += display.get(Tile(x, y), ' ')
            display_str += '\n'

        display_str += f'Score: {self.score}\n'
        if self.result == 'lost':
            display_str += 'Game Over\n'
        elif self.result == 'won':
            display_str += 'Winner!\n'

        return display_str

    def update(self) -> None:
        for i in range(0, len(self.computer.output), 3):
            x: int = self.computer.output[i]
            y: int = self.computer.output[i + 1]

            if (x, y) == (-1, 0):
                self.score = self.computer.output[i + 2]
            else:
                tile_id: int = self.computer.output[i + 2]
                if tile_id == 0:
                    self.blocks.discard(Tile(x, y))
                elif tile_id == 1:
                    self.walls.add(Tile(x, y))
                elif tile_id == 2:
                    self.blocks.add(Tile(x, y))
                elif tile_id == 3:
                    self.paddle = Tile(x, y)
                elif tile_id == 4:
                    self.ball = Tile(x, y)

        if self.right_wall == 0:
            self.right_wall = max(wall.x for wall in self.walls) - 1
        if self.ball.y == self.paddle.y:
            self.result = 'lost'
        if not self.blocks:
            self.result = 'won'

    def play(self) -> None:
        self.computer.execute(self.program)
        self.update()

    def joystick(self, position: int) -> None:
        self.computer.run([position])
        self.update()

    def next_joystick(self) -> int:
        # Wall bounces
        if self.ball.y < self.paddle.y - 1:
            if self.ball.x == self.left_wall:
                return 1
            if self.ball.x == self.right_wall:
                return -1

        if self.ball.x < self.paddle.x:
            return -1
        if self.ball.x > self.paddle.x:
            return 1
        return 0


def part1(data):
    """Solve part 1"""
    game: BrickGame = BrickGame(data)
    game.play()
    return len(game.blocks)


def part2(data):
    """Solve part 2"""
    data[0] = 2

    game: BrickGame = BrickGame(data)
    game.play()
    while not game.result:
        direction: int = game.next_joystick()
        game.joystick(direction)
        # print(game)
    return game.score


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
