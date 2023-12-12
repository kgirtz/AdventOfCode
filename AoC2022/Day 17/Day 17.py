import pathlib
import sys
import os
from enum import Enum
from collections import namedtuple

Point = namedtuple('Point', 'x y')


class BlockType(Enum):
    HBAR = 0
    PLUS = 1
    L = 2
    VBAR = 3
    SQUARE = 4


class Block:
    block_widths: dict[BlockType, int] = {BlockType.HBAR:   4,
                                          BlockType.PLUS:   3,
                                          BlockType.L:      3,
                                          BlockType.VBAR:   1,
                                          BlockType.SQUARE: 2}
    height_offset: dict[BlockType, int] = {BlockType.HBAR:   0,
                                           BlockType.PLUS:   1,
                                           BlockType.L:      2,
                                           BlockType.VBAR:   3,
                                           BlockType.SQUARE: 1}

    def __init__(self, typ: BlockType, x: int, y: int) -> None:
        self.type: BlockType = typ
        self.x: int = x
        self.y: int = y

    def width(self) -> int:
        return self.block_widths[self.type]

    def high_point(self) -> int:
        return self.y + self.height_offset[self.type]

    def points_on_rock(self) -> set[Point]:
        match self.type:
            case BlockType.HBAR:
                return {Point(self.x + i, self.y) for i in range(4)}
            case BlockType.PLUS:
                plus_pts: set[Point] = {Point(self.x + i, self.y) for i in range(3)}
                plus_pts |= {Point(self.x + 1, self.y - 1 + i) for i in range(3)}
                return plus_pts
            case BlockType.L:
                l_pts: set[Point] = {Point(self.x + i, self.y) for i in range(3)}
                l_pts |= {Point(self.x + 2, self.y + i) for i in range(3)}
                return l_pts
            case BlockType.VBAR:
                return {Point(self.x, self.y + i) for i in range(4)}
            case BlockType.SQUARE:
                return {Point(self.x + i, self.y + j) for i in range(2) for j in range(2)}

    def fall(self, num_spaces: int = 1) -> None:
        self.y -= num_spaces

    def blow_sideways(self, direction: str, fixed: set[Point], right_wall: int) -> None:
        # Blow left
        if direction == '<':
            if self.x > 0 and not self.blocked_on_left(fixed):
                self.x -= 1
        # Blow right
        else:
            if self.x + self.width() < right_wall and not self.blocked_on_right(fixed):
                self.x += 1

    def blocked_on_left(self, fixed: set[Point]) -> bool:
        match self.type:
            case BlockType.HBAR:
                return (self.x - 1, self.y) in fixed
            case BlockType.PLUS:
                return (self.x - 1, self.y) in fixed or \
                       (self.x, self.y + 1) in fixed or \
                       (self.x, self.y - 1) in fixed
            case BlockType.L:
                return (self.x - 1, self.y) in fixed or \
                       (self.x + 1, self.y + 1) in fixed or \
                       (self.x + 1, self.y + 2) in fixed
            case BlockType.VBAR:
                return any((self.x - 1, self.y + i) in fixed for i in range(4))
            case BlockType.SQUARE:
                return any((self.x - 1, self.y + i) in fixed for i in range(2))

    def blocked_on_right(self, fixed: set[Point]) -> bool:
        match self.type:
            case BlockType.HBAR:
                return (self.x + 4, self.y) in fixed
            case BlockType.PLUS:
                return (self.x + 3, self.y) in fixed or \
                       (self.x + 2, self.y + 1) in fixed or \
                       (self.x + 2, self.y - 1) in fixed
            case BlockType.L:
                return any((self.x + 3, self.y + i) in fixed for i in range(3))
            case BlockType.VBAR:
                return any((self.x + 1, self.y + i) in fixed for i in range(4))
            case BlockType.SQUARE:
                return any((self.x + 2, self.y + i) in fixed for i in range(2))

    def blocked_below(self, fixed: set[Point]) -> bool:
        match self.type:
            case BlockType.HBAR:
                return any((self.x + i, self.y - 1) in fixed for i in range(4))
            case BlockType.PLUS:
                return (self.x, self.y - 1) in fixed or \
                       (self.x + 1, self.y - 2) in fixed or \
                       (self.x + 2, self.y - 1) in fixed
            case BlockType.L:
                return any((self.x + i, self.y - 1) in fixed for i in range(3))
            case BlockType.VBAR:
                return (self.x, self.y - 1) in fixed
            case BlockType.SQUARE:
                return any((self.x + i, self.y - 1) in fixed for i in range(2))


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.strip()


def spawn_rock(left: int, bottom: int, rock_type_idx: int) -> Block:
    block_type: BlockType = BlockType(rock_type_idx)

    if block_type == BlockType.PLUS:
        return Block(block_type, left, bottom + 1)

    return Block(block_type, left, bottom)


def print_rocks(fixed: set[Point], max_height: int, chasm_width: int) -> None:
    chasm: list[str] = ['' for _ in range(max_height + 2)]
    chasm[0] = '+' + '-' * chasm_width + '+'

    for y in range(max_height + 1):
        chasm[y + 1] += '|'
        for x in range(chasm_width):
            if (x, y) in fixed:
                chasm[y + 1] += '#'
            else:
                chasm[y + 1] += '.'
        chasm[y + 1] += '|'

    for row in chasm[::-1]:
        print(row)
    print()


def height_after_n_rocks(n: int, jets: str) -> int:
    jet_idx: int = 0

    chasm_width: int = 7
    max_height: int = -1
    rocks: set[Point] = {Point(x, -1) for x in range(chasm_width)}  # floor
    rock_idx: int = 0

    for _ in range(n):
        # Produce new rock just above max height
        cur_rock: Block = spawn_rock(2, max_height + 1, rock_idx)
        rock_idx = (rock_idx + 1) % len(BlockType)

        # Execute next 4 sideways shifts
        for _ in range(4):
            cur_rock.blow_sideways(jets[jet_idx], rocks, chasm_width)
            jet_idx = (jet_idx + 1) % len(jets)

        while not cur_rock.blocked_below(rocks):
            cur_rock.fall()
            cur_rock.blow_sideways(jets[jet_idx], rocks, chasm_width)
            jet_idx = (jet_idx + 1) % len(jets)

        max_height = max(max_height, cur_rock.high_point())
        rocks |= cur_rock.points_on_rock()

    return max_height + 1


def height_after_big_n_rocks(n: int, jets: str) -> int:
    jet_idx: int = 0

    chasm_width: int = 7
    max_height: int = -1
    rocks: set[Point] = {Point(x, -1) for x in range(chasm_width)}  # floor
    rock_idx: int = 0
    num_rocks: int = 0

    jet_offsets: dict[int, tuple[int, int]] = {}
    while True:
        if rock_idx == 0:
            if jet_idx in jet_offsets:
                num_base_rocks, base_height = jet_offsets[jet_idx]
                num_stream_rocks: int = num_rocks - num_base_rocks
                stream_height: int = max_height - base_height
                break
            else:
                jet_offsets[jet_idx] = (num_rocks, max_height)

        num_rocks += 1

        # Produce new rock just above max height
        cur_rock: Block = spawn_rock(2, max_height + 1, rock_idx)
        rock_idx = (rock_idx + 1) % len(BlockType)

        # Execute next 4 sideways shifts
        for _ in range(4):
            cur_rock.blow_sideways(jets[jet_idx], rocks, chasm_width)
            jet_idx = (jet_idx + 1) % len(jets)

        while not cur_rock.blocked_below(rocks):
            cur_rock.fall()
            cur_rock.blow_sideways(jets[jet_idx], rocks, chasm_width)
            jet_idx = (jet_idx + 1) % len(jets)

        max_height = max(max_height, cur_rock.high_point())
        rocks |= cur_rock.points_on_rock()

    num_streams: int = (n - num_base_rocks) // num_stream_rocks
    partial_stream_rocks: int = (n - num_base_rocks) % num_stream_rocks
    partial_stream_height: int = height_after_n_rocks(num_base_rocks + partial_stream_rocks, jets)
    return num_streams * stream_height + partial_stream_height


def part1(data):
    """Solve part 1"""

    return height_after_n_rocks(2022, data)


def part2(data):
    """Solve part 2"""

    return height_after_big_n_rocks(1000000000000, data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
