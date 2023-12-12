import pathlib
import sys
import os
from collections import namedtuple, defaultdict

Point = namedtuple('Point', 'x y')

sys.path.append('..')
from intcode import IntcodeComputer


class VacuumDroid:
    origin: Point = Point(0, 0)
    OPPOSITE_DIR: dict[str, str] = {'^': 'v', 'v': '^', '<': '>', '>': '<'}
    TURN_RIGHT: dict[str, str] = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
    TURN_LEFT: dict[str, str] = {'^': '<', '>': '^', 'v': '>', '<': 'v'}

    def __init__(self, program: list[int]) -> None:
        self.computer: IntcodeComputer = IntcodeComputer()
        self.program: list[int] = program

        self.cur_pos: Point = Point(0, 0)
        self.cur_dir: str = '^'

        self.scaffolding: set[Point] = set()
        self.computer.execute(self.program)
        self.width: int = self.computer.output_ASCII().index('\n')
        self.height: int = len(self.computer.output) // self.width

        x, y = 0, 0
        for ch in self.computer.output_ASCII():
            match ch:
                case '#':
                    self.scaffolding.add(Point(x, y))
                case '^' | 'v' | '<' | '>':
                    self.scaffolding.add(Point(x, y))
                    self.cur_pos = Point(x, y)
                    self.cur_dir = ch
                case '\n':
                    y += 1
                    x = -1
            x += 1

        self.intersections: set[Point] = set()
        self.dead_ends: set[Point] = set()
        self.corners: set[Point] = set()
        for s in self.scaffolding:
            neighbors: set[Point] = self.scaffold_neighbors(s)
            match len(neighbors):
                case 1:
                    self.dead_ends.add(s)
                case 2:
                    s1, s2 = neighbors
                    if s1.x != s2.x and s1.y != s2.y:
                        self.corners.add(s)
                case _:
                    self.intersections.add(s)
        self.endpoints: set[Point] = self.intersections | self.corners | self.dead_ends

    def move(self, distance: int) -> None:
        x, y = self.cur_pos
        match self.cur_dir:
            case '^':
                y -= distance
            case 'v':
                y += distance
            case '<':
                x -= distance
            case '>':
                x += distance
        self.cur_pos = Point(x, y)

    def scaffold_neighbors(self, s: Point) -> set[Point]:
        assert s in self.scaffolding

        neighbors: set[Point] = set()
        if s.y > 0:
            neighbors.add(Point(s.x, s.y - 1))
        if s.y < self.height - 1:
            neighbors.add(Point(s.x, s.y + 1))
        if s.x > 0:
            neighbors.add(Point(s.x - 1, s.y))
        if s.x < self.width - 1:
            neighbors.add(Point(s.x + 1, s.y))
        return neighbors & self.scaffolding

    def exit_directions(self, s: Point, entry_dir: str = '') -> set[str]:
        exits: set[str] = set()
        for n in self.scaffold_neighbors(s):
            if n.y < s.y:
                exits.add('^')
            elif n.y > s.y:
                exits.add('v')
            elif n.x < s.x:
                exits.add('<')
            elif n.x > s.x:
                exits.add('>')

        if entry_dir:
            exits.remove(self.OPPOSITE_DIR[entry_dir])

        return exits

    def all_segment_lengths(self) -> dict[int, int]:
        lengths: defaultdict[int, int] = defaultdict(int)
        to_check: dict[Point, set[str]] = {}
        for s in self.endpoints:
            to_check[s] = self.exit_directions(s)

        for c in self.corners:
            for direction in to_check[c]:
                length: int = self.segment_length(c, direction)
                other_end: Point = self.segment_endpoint(c, direction)
                lengths[length] += 1
                to_check[other_end].remove(self.OPPOSITE_DIR[direction])
            to_check[c].clear()

        for i in self.intersections:
            for direction in to_check[i]:
                length = self.segment_length(i, direction)
                lengths[length] += 1

        return dict(lengths)

    def segment_length(self, origin: Point, direction: str) -> int:
        length: int = 0
        x, y = origin
        while (x, y) in self.scaffolding:
            length += 1
            match direction:
                case '^':
                    y -= 1
                case 'v':
                    y += 1
                case '<':
                    x -= 1
                case '>':
                    x += 1

        return length

    def segment_endpoint(self, origin: Point, direction: str) -> Point:
        x, y = origin
        match direction:
            case '^':
                y -= self.segment_length(origin, direction) - 1
            case 'v':
                y += self.segment_length(origin, direction) - 1
            case '<':
                x -= self.segment_length(origin, direction) - 1
            case '>':
                x += self.segment_length(origin, direction) - 1

        assert (x, y) in (self.corners | self.dead_ends)
        return Point(x, y)

    def corner_lengths(self) -> dict[int, int]:
        lengths: defaultdict[tuple[int, int], int] = defaultdict(int)
        for c in self.corners:
            exits: set[str] = self.exit_directions(c)
            for direction in exits:
                if self.TURN_RIGHT[direction] in exits:
                    left_len: int = self.segment_length(c, direction)
                    right_len: int = self.segment_length(c, self.TURN_RIGHT[direction])
                    lengths[(right_len, left_len)] += 1
                    break
        return dict(lengths)

    @staticmethod
    def alignment_parameter(s: Point) -> int:
        return s.x * s.y

    def visit_every_point(self) -> list[str]:
        steps: list[str] = []

        # Start at dead end
        vector: str = self.exit_directions(self.cur_pos).pop()
        if vector == self.TURN_RIGHT[self.cur_dir]:
            steps.append('R')
            self.cur_dir = self.TURN_RIGHT[self.cur_dir]
        elif vector == self.TURN_LEFT[self.cur_dir]:
            steps.append('L')
            self.cur_dir = self.TURN_LEFT[self.cur_dir]

        # Move off dead end
        d: int = self.segment_length(self.cur_pos, self.cur_dir)
        self.move(d - 1)
        steps.append(str(d - 1))

        while self.cur_pos not in self.dead_ends:
            vector = (self.exit_directions(self.cur_pos, self.cur_dir)).pop()
            if vector == self.TURN_RIGHT[self.cur_dir]:
                steps.append('R')
                self.cur_dir = self.TURN_RIGHT[self.cur_dir]
            elif vector == self.TURN_LEFT[self.cur_dir]:
                steps.append('L')
                self.cur_dir = self.TURN_LEFT[self.cur_dir]

            d = self.segment_length(self.cur_pos, self.cur_dir)
            self.move(d - 1)
            steps.append(str(d - 1))

        return steps

    @staticmethod
    def functions_cover_whole_path(a: list[str], b: list[str], c: list[str], actions: list[str]) -> bool:
        if not actions:
            return True
        if a == actions[:len(a)]:
            return VacuumDroid.functions_cover_whole_path(a, b, c, actions[len(a):])
        if b == actions[:len(b)]:
            return VacuumDroid.functions_cover_whole_path(a, b, c, actions[len(b):])
        if c == actions[:len(c)]:
            return VacuumDroid.functions_cover_whole_path(a, b, c, actions[len(c):])
        return False

    @staticmethod
    def get_main_routine_str(funcs: list[str], actions: str) -> str:
        main_routine: str = actions
        for f, name in zip(funcs, ('A', 'B', 'C')):
            main_routine = main_routine.replace(f, name)
        return main_routine

    @staticmethod
    def divide_into_functions(actions: list[str]) -> list[str]:
        for a_end in range(10):
            a: list[str] = actions[:a_end + 1]
            b_start: int = a_end + 1
            while a == actions[b_start:b_start + len(a)]:
                b_start += len(a)

            for b_end in range(b_start, b_start + 10):
                b: list[str] = actions[b_start:b_end + 1]
                c_start: int = b_end + 1
                while True:
                    if a == actions[c_start:c_start + len(a)]:
                        c_start += len(a)
                    elif b == actions[c_start:c_start + len(b)]:
                        c_start += len(b)
                    else:
                        break

                for c_end in range(c_start, c_start + 10):
                    c: list[str] = actions[c_start:c_end + 1]

                    if VacuumDroid.functions_cover_whole_path(a, b, c, actions):
                        funcs: list[str] = [','.join(f) for f in (a, b, c)]
                        if all(len(f) <= 20 for f in funcs):
                            main_routine: str = VacuumDroid.get_main_routine_str(funcs, ','.join(actions))
                            return [main_routine] + funcs

        return ['', '', '', '']

    def visit_all_scaffolding(self, continuous_feed: bool = False) -> int:
        actions: list[str] = self.visit_every_point()
        main_routine, func_a, func_b, func_c = VacuumDroid.divide_into_functions(actions)

        # Pack inputs into single list
        cmd: str = '\n'.join((main_routine, func_a, func_b, func_c)) + '\n'
        cmd += ('y' if continuous_feed else 'n') + '\n'

        # Run modified program with input and return output
        self.program[0] = 2
        self.computer.execute(self.program)  # Run to get first video feed
        # print(self.computer.output_ASCII())
        self.computer.run_ASCII(cmd)  # Run with movement commands
        # print(self.computer.output_ASCII())
        dust: int = self.computer.output[-1]
        self.program[0] = 1

        return dust


def parse(puzzle_input):
    """Parse input"""
    return [int(num) for num in puzzle_input.split(',')]


def part1(data):
    """Solve part 1"""
    droid: VacuumDroid = VacuumDroid(data)
    return sum(VacuumDroid.alignment_parameter(s) for s in droid.intersections)


def part2(data):
    """Solve part 2"""
    droid: VacuumDroid = VacuumDroid(data)
    dust: int = droid.visit_all_scaffolding()
    return dust


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
