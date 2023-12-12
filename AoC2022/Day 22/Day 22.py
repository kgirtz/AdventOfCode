import pathlib
import sys
import os
from collections import namedtuple
from typing import Optional, Union
from copy import deepcopy

Point = namedtuple('Point', 'x y')
Region = namedtuple('Region', 'xmin xmax ymin ymax')

ROTATIONS: dict[str, dict[str, str]] = {'>': {'>': 'v', '<': '^'},
                                        '<': {'>': '^', '<': 'v'},
                                        '^': {'>': '>', '<': '<'},
                                        'v': {'>': '<', '<': '>'}}


class Position:
    def __init__(self, *args) -> None:
        if len(args) == 3:
            x, y, heading = args
        elif len(args) == 2:
            (x, y), heading = args
        else:
            x, y, heading = 0, 0, ''

        self.x: int = x
        self.y: int = y
        self.heading: str = heading

    def __repr__(self) -> str:
        return str((self.x, self.y, self.heading))

    def password(self) -> int:
        return 1000 * (self.y + 1) + 4 * (self.x + 1) + {'>': 0, 'v': 1, '<': 2, '^': 3}[self.heading]

    def turn(self, direction: str) -> None:
        self.heading = ROTATIONS[self.heading][direction]

    def update_heading(self, s: 'Side') -> None:
        i: int = s.origin.sides.index(s)
        self.heading = ['v', '<', '^', '>'][i]

    def move(self, distance: int, board: 'Board', mode: str = '') -> None:
        for _ in range(distance):
            target: Position = board.get_target(self, mode)
            if (target.x, target.y) in board.walls:
                return

            self.x, self.y, self.heading = target.x, target.y, target.heading


class Board:
    def __init__(self, board_str: str) -> None:
        self.walls: set[Point] = set()
        self.regions: list[Region] = []
        self.cube: list[Face] = []

        self.extract_regions(board_str)
        self.build_cube_from_regions()

    def get_side_length(self) -> int:
        return self.regions[0].ymax - self.regions[0].ymin + 1

    def get_region_idx(self, y: int) -> int:
        for i, region in enumerate(self.regions):
            if region.ymin <= y <= region.ymax:
                return i

    def get_cur_face(self, pos: Point | Position) -> 'Face':
        for face in self.cube:
            if pos in face:
                return face

    def get_transfer_edge(self, pos: Point | Position) -> tuple['Side', 'Side']:
        cur_face: Face = self.get_cur_face(pos)
        i: int = ['^', '>', 'v', '<'].index(pos.heading)
        s: Side = cur_face.sides[i]
        return s, s.face.get_side(cur_face)

    def transfer_region_down(self, pos: Position) -> int:
        r: int = self.get_region_idx(pos.y)
        region_below: Region = self.regions[(r + 1) % len(self.regions)]
        if region_below.xmin <= pos.x <= region_below.xmax:
            return pos.y + 1

        region_above: Region = self.regions[r]
        while region_above.xmin <= pos.x <= region_above.xmax:
            r = (r - 1) % len(self.regions)
            region_above = self.regions[r]

        return self.regions[(r + 1) % len(self.regions)].ymin

    def transfer_region_up(self, pos: Position) -> int:
        r: int = self.get_region_idx(pos.y)
        region_above: Region = self.regions[(r - 1) % len(self.regions)]
        if region_above.xmin <= pos.x <= region_above.xmax:
            return pos.y - 1

        region_below: Region = self.regions[r]
        while region_below.xmin <= pos.x <= region_below.xmax:
            r = (r + 1) % len(self.regions)
            region_below = self.regions[r]

        return self.regions[(r - 1) % len(self.regions)].ymax

    def move_around_cube(self, pos: Position) -> Position:
        source_side, dest_side = self.get_transfer_edge(pos)
        new_pt: Point = dest_side.pt_relative_to_end(source_side.dist_from_start(pos))
        new_pos: Position = Position(new_pt, '')
        new_pos.update_heading(dest_side)
        return new_pos

    def get_target(self, pos: Position, mode: str) -> Position:
        x, y = pos.x, pos.y

        if mode == 'cube':
            cur_face: Face = self.get_cur_face(pos)
            match pos.heading:
                case '<':
                    if pos.x == cur_face.bounds.xmin:
                        return self.move_around_cube(pos)
                    else:
                        x -= 1
                case '>':
                    if pos.x == cur_face.bounds.xmax:
                        return self.move_around_cube(pos)
                    else:
                        x += 1
                case 'v':
                    if pos.y == cur_face.bounds.ymax:
                        return self.move_around_cube(pos)
                    else:
                        y += 1
                case '^':
                    if pos.y == cur_face.bounds.ymin:
                        return self.move_around_cube(pos)
                    else:
                        y -= 1
        else:
            cur_region: int = self.get_region_idx(pos.y)
            match pos.heading:
                case '<':
                    if x == self.regions[cur_region].xmin:
                        x = self.regions[cur_region].xmax
                    else:
                        x -= 1
                case '>':
                    if x == self.regions[cur_region].xmax:
                        x = self.regions[cur_region].xmin
                    else:
                        x += 1
                case 'v':
                    if y == self.regions[cur_region].ymax:
                        y = self.transfer_region_down(pos)
                    else:
                        y += 1
                case '^':
                    if y == self.regions[cur_region].ymin:
                        y = self.transfer_region_up(pos)
                    else:
                        y -= 1

        return Position(x, y, pos.heading)

    def extract_regions(self, board_str: str) -> None:
        # Pad first line with spaces
        board_lines: list[str] = board_str.split('\n')
        board_lines[0] = ' ' * board_lines[1].count(' ') + board_lines[0]

        prev_min_x, prev_max_x = -1, -1
        min_y = 0
        for y, line in enumerate(board_lines):
            min_x, max_x = -1, -1
            for x, pos in enumerate(line):
                if min_x < 0 and pos != ' ':
                    min_x = x
                if max_x < 0 and min_x >= 0 and pos == ' ':
                    max_x = x
                if pos == '#':
                    self.walls.add(Point(x, y))
            if max_x <= 0:
                max_x = len(line) - 1

            if (min_x, max_x) != (prev_min_x, prev_max_x) and y > 0:
                self.regions.append(Region(prev_min_x, prev_max_x, min_y, y - 1))
                min_y = y

            prev_min_x, prev_max_x = min_x, max_x

        self.regions.append(Region(prev_min_x, prev_max_x, min_y, len(board_lines) - 1))

    def build_cube_from_regions(self) -> None:
        n: int = self.get_side_length()

        # Split regions into faces
        r: int = 0
        face_dict: dict[Point, Face] = {}
        for y in range(0, 6 * n, n):
            for x in range(0, 6 * n, n):
                if x > self.regions[r].xmax:
                    r += 1
                    break
                if self.regions[r].xmin <= x:
                    face_dict[Point(x, y)] = Face(x, y, n)
            if r == len(self.regions):
                break

        # Connect faces along edges if pre-connected
        for (x, y), face in face_dict.items():
            if (x, y - n) in face_dict:  # above
                face.sides[0].face = face_dict[(x, y - n)]
            if (x + n, y) in face_dict:  # right
                face.sides[1].face = face_dict[(x + n, y)]
            if (x, y + n) in face_dict:  # below
                face.sides[2].face = face_dict[(x, y + n)]
            if (x - n, y) in face_dict:  # left
                face.sides[3].face = face_dict[(x - n, y)]

        # Fold cube together and connect simple sides
        self.cube = list(face_dict.values())
        sides_to_connect: list[tuple[Side, Side]] = []
        for f in self.cube:
            if f.connected_sides() < 2:
                continue
            for s in f.sides:
                if not s.is_connected():
                    continue
                s_cw: Side = f.get_side_clockwise(s)
                if not s_cw.is_connected():
                    continue

                left: Side = s.face.get_side_counterclockwise(f)
                right: Side = s_cw.face.get_side_clockwise(f)
                sides_to_connect.append((left, right))

        for s1, s2 in sides_to_connect:
            s1.face = s2.origin
            s2.face = s1.origin

        # Connect arbitrary sides
        self.connect_cube_faces()

    def connect_cube_faces(self) -> bool:
        simulate: bool = False
        while not all(f.connected_sides() == 4 for f in self.cube):
            side_connected: bool = False
            for i, f in enumerate(self.cube):
                for s in f.sides:
                    if not s.is_connected():
                        continue
                    s_cw: Side = f.get_side_clockwise(s)
                    if not s_cw.is_connected():
                        continue

                    if s_cw.face in s.face.get_adjacent_faces():
                        continue

                    left_sides: list[Side] = [ls for ls in s.face.get_adjacent_sides(f) if not ls.is_connected()]
                    right_sides: list[Side] = [rs for rs in s_cw.face.get_adjacent_sides(f) if not rs.is_connected()]

                    if len(left_sides) == len(right_sides) == 1:
                        left: Side = left_sides[0]
                        right: Side = right_sides[0]
                        left.face = right.origin
                        right.face = left.origin
                        side_connected = True

                    elif simulate and left_sides and right_sides:
                        for left in left_sides:
                            for right in right_sides:
                                left.face = right.origin
                                right.face = left.origin

                                # Copy faces and recurse
                                backup: list[Face] = self.cube
                                self.cube = deepcopy(self.cube)
                                if self.connect_cube_faces():
                                    return True
                                else:
                                    self.cube = backup
                                    left.face = None
                                    right.face = None
                                    left.flipped = False
                                    right.flipped = False
                    else:
                        pass
            if simulate and not side_connected:
                return False
            simulate = not side_connected

        return True


class Side:
    def __init__(self, start: Point, end: Point, face: 'Face') -> None:
        self.origin: Face = face
        self.face: Optional[Face] = None
        self.start: Point = start
        self.end: Point = end

    def __contains__(self, item: Point | Position) -> bool:
        return min(self.start.x, self.end.x) <= item.x <= max(self.start.x, self.end.x) and \
                    min(self.start.y, self.end.y) <= item.y <= max(self.start.y, self.end.y)

    def is_connected(self) -> bool:
        return self.face is not None

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def dist_from_start(self, pos: Point | Position) -> int:
        if self.is_vertical():
            return max(pos.y, self.start.y) - min(pos.y, self.start.y)
        else:
            return max(pos.x, self.start.x) - min(pos.x, self.start.x)

    def pt_relative_to_end(self, distance: int) -> Point:
        if self.is_vertical():
            y: int = self.end.y - distance if self.end.y > self.start.y else self.end.y + distance
            return Point(self.end.x, y)
        else:
            x: int = self.end.x - distance if self.end.x > self.start.x else self.end.x + distance
            return Point(x, self.end.y)


class Face:
    def __init__(self, xmin: int, ymin: int, n: int) -> None:
        self.bounds: Region = Region(xmin, xmin + n - 1, ymin, ymin + n - 1)
        self.upper_left: Point = Point(xmin, ymin)
        self.upper_right: Point = Point(xmin + n - 1, ymin)
        self.lower_left: Point = Point(xmin, ymin + n - 1)
        self.lower_right: Point = Point(xmin + n - 1, ymin + n - 1)

        # first is top, moving around clockwise
        self.sides: list[Side] = [Side(self.upper_left, self.upper_right, self),
                                  Side(self.upper_right, self.lower_right, self),
                                  Side(self.lower_right, self.lower_left, self),
                                  Side(self.lower_left, self.upper_left, self)]

    def __str__(self) -> str:
        face_str: str = str(self.bounds) + '\n'
        face_str += f'\t{self.connected_sides()} sides connected\n'
        for s in self.sides:
            if s.is_connected():
                face_str += f'\t{s}\n'
        return face_str

    def __contains__(self, item: Position | Point) -> bool:
        return (self.bounds.xmin <= item.x <= self.bounds.xmax) and (self.bounds.ymin <= item.y <= self.bounds.ymax)

    def get_adjacent_faces(self) -> list[Union['Face', None]]:
        # Indices correspond to self.sides
        return [s.face for s in self.sides]

    def connected_sides(self) -> int:
        return 4 - self.get_adjacent_faces().count(None)

    def get_side(self, f: 'Face') -> Optional[Side]:
        for s in self.sides:
            if s.face is f:
                return s
        return None

    def get_side_clockwise(self, s: Union[Side, 'Face']) -> Side:
        if type(s) is Side:
            return self.sides[(self.sides.index(s) + 1) % 4]
        elif type(s) is Face:
            faces: list[Face] = self.get_adjacent_faces()
            return self.sides[(faces.index(s) + 1) % 4]

    def get_side_counterclockwise(self, s: Union[Side, 'Face']) -> Side:
        if type(s) is Side:
            return self.sides[(self.sides.index(s) - 1) % 4]
        elif type(s) is Face:
            faces: list[Face] = self.get_adjacent_faces()
            return self.sides[(faces.index(s) - 1) % 4]

    def get_adjacent_sides(self, s: Union[Side, 'Face']) -> list['Side']:
        return [self.get_side_clockwise(s), self.get_side_counterclockwise(s)]


def parse(puzzle_input):
    """Parse input"""
    board_str, path = puzzle_input.split('\n\n')
    board: Board = Board(board_str)

    return board, list(tokenize(path))


def tokenize(path: str) -> list[str]:
    i: int = 0
    while i < len(path):
        match path[i]:
            case 'R':
                i += 1
                yield '>'
            case 'L':
                i += 1
                yield '<'
            case _:
                j: int = i + 1
                while j < len(path) and path[j].isdigit():
                    j += 1
                yield path[i:j]
                i = j


def part1(data):
    """Solve part 1"""
    board, path = data

    cur_pos: Position = Position(board.regions[0].xmin, 0, '>')

    for instruction in path:
        match instruction:
            case '<' | '>':
                cur_pos.turn(instruction)
            case _:
                cur_pos.move(int(instruction), board)

    return cur_pos.password()


def part2(data):
    """Solve part 2"""
    board, path = data

    cur_pos: Position = Position(board.regions[0].xmin, 0, '>')

    for instruction in path:
        match instruction:
            case '<' | '>':
                cur_pos.turn(instruction)
            case _:
                cur_pos.move(int(instruction), board, 'cube')

    return cur_pos.password()


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
