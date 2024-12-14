import pathlib
import sys
import os
from xypair import XYpair


class Surface:
    def __init__(self, surface_str: list[str]) -> None:
        self.start: XYpair = XYpair()
        self.height: int = len(surface_str)
        self.width: int = len(surface_str[0])
        self.tiles: list[str] = surface_str
        self.loop: set[XYpair] = set()

        # Find starting pipe
        for y, line in enumerate(surface_str):
            for x, tile in enumerate(line):
                if tile == 'S':
                    self.start = XYpair(x, y)
                    break

        # Determine starting pipe type
        pipe_types: set[str] = {'|', '-', 'L', 'F', 'J', '7'}
        if self.start not in self.connections(self.start.up()):
            pipe_types -= {'|', 'L', 'J'}
        if self.start not in self.connections(self.start.down()):
            pipe_types -= {'|', '7', 'F'}
        if self.start not in self.connections(self.start.left()):
            pipe_types -= {'-', '7', 'J'}
        if self.start not in self.connections(self.start.right()):
            pipe_types -= {'-', 'L', 'F'}

        assert len(pipe_types) == 1
        self.tiles[self.start.y] = self.tiles[self.start.y].replace('S', pipe_types.pop())

        # Explore rest of the loop
        self.loop = {self.start}
        cur_pipe, end_pipe = self.connections(self.start)
        while cur_pipe != end_pipe:
            self.loop.add(cur_pipe)
            cur_pipe = [pipe for pipe in self.connections(cur_pipe) if pipe not in self.loop][0]
        self.loop.add(end_pipe)

    def tile_at(self, pt: XYpair) -> str:
        return self.tiles[pt.y][pt.x]

    def valid_point(self, pt: XYpair) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def on_edge(self, pt: XYpair) -> bool:
        return pt.x in (0, self.width - 1) or pt.y in (0, self.height - 1)

    def neighbors(self, pt: XYpair) -> set[XYpair]:
        return {n for n in pt.neighbors() if self.valid_point(n)}

    def connections(self, pt: XYpair) -> list[XYpair]:
        if not self.valid_point(pt):
            return []

        connected_pipes: list[XYpair] = []

        tile: str = self.tile_at(pt)
        if tile in ('|', 'J', 'L'):
            connected_pipes.append(pt.up())
        if tile in ('|', 'F', '7'):
            connected_pipes.append(pt.down())
        if tile in ('-', 'J', '7'):
            connected_pipes.append(pt.left())
        if tile in ('-', 'F', 'L'):
            connected_pipes.append(pt.right())

        return [pipe for pipe in connected_pipes if self.valid_point(pipe)]

    def max_loop_distance(self) -> int:
        loop: set[XYpair] = {self.start}
        left, right = self.connections(self.start)
        distance: int = 1

        while left != right and left not in self.connections(right):
            next_left: XYpair = [pipe for pipe in self.connections(left) if pipe not in loop][0]
            next_right: XYpair = [pipe for pipe in self.connections(right) if pipe not in loop][0]

            loop |= {left, right}
            left = next_left
            right = next_right
            distance += 1

        return distance

    def inside(self, prev: XYpair, cur: XYpair) -> set[XYpair]:
        if not (self.valid_point(prev) and self.valid_point(cur)):
            return set()

        if prev == cur.down():
            match self.tile_at(cur):
                case '|':
                    return {cur.right()}
                case 'F':
                    return {cur.down_right()}
                case '7':
                    return {cur.right(), cur.up(), cur.up_right()}

        elif prev == cur.up():
            match self.tile_at(cur):
                case '|':
                    return {cur.left()}
                case 'L':
                    return {cur.left(), cur.down(), cur.down_left()}
                case 'J':
                    return {cur.up_left()}

        elif prev == cur.left():
            match self.tile_at(cur):
                case '-':
                    return {cur.down()}
                case 'J':
                    return {cur.down(), cur.right(), cur.down_right()}
                case '7':
                    return {cur.down_left()}

        elif prev == cur.right():
            match self.tile_at(cur):
                case '-':
                    return {cur.up()}
                case 'F':
                    return {cur.up(), cur.left(), cur.up_left()}
                case 'L':
                    return {cur.up_right()}

        return set()

    def explore_area(self, tile: XYpair) -> set[XYpair]:
        if tile in self.loop:
            return set()

        area: set[XYpair] = set()
        to_explore: set[XYpair] = {tile}
        while to_explore:
            cur_tile: XYpair = to_explore.pop()
            to_explore |= self.neighbors(cur_tile) - area - self.loop
            area.add(cur_tile)

        return area

    def enclosed_loop_area(self) -> set[XYpair]:
        for pipe in self.connections(self.start):
            prev_pipe: XYpair = self.start
            cur_pipe: XYpair = pipe
            enclosed: set[XYpair] = set()

            while cur_pipe != self.start:
                inside_tiles: set[XYpair] = self.inside(prev_pipe, cur_pipe)
                new_enclosed: set[XYpair] = set()
                for pt in inside_tiles - enclosed:
                    new_enclosed |= self.explore_area(pt)
                if not inside_tiles or any(self.on_edge(ex) for ex in new_enclosed):
                    break
                enclosed |= new_enclosed

                backwards: XYpair = prev_pipe
                prev_pipe = cur_pipe
                cur_pipe = [tile for tile in self.connections(cur_pipe) if tile != backwards][0]

            # Final loop iteration
            if cur_pipe == self.start:
                inside_tiles = self.inside(prev_pipe, cur_pipe)
                new_enclosed: set[XYpair] = set()
                for pt in inside_tiles - enclosed:
                    new_enclosed |= self.explore_area(pt)
                if not inside_tiles or any(self.on_edge(ex) for ex in new_enclosed):
                    continue

                return enclosed


def parse(puzzle_input):
    """Parse input"""
    return Surface(puzzle_input.split('\n'))


def part1(data):
    """Solve part 1"""
    return data.max_loop_distance()


def part2(data):
    """Solve part 2"""
    return len(data.enclosed_loop_area())


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 8
    PART2_TEST_ANSWER = 10

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
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

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
