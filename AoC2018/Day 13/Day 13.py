import pathlib
import sys
import os
import itertools
from collections.abc import Iterator

from space import Space
from xypair import XYpair
from pointwalker import PointWalker, Heading


class Cart:
    def __init__(self, position: XYpair, heading: str) -> None:
        self.walker: PointWalker = PointWalker(position, Heading.from_arrow(heading))
        self.turn_iter: Iterator[str] = itertools.cycle(('LEFT', 'FORWARD', 'RIGHT'))
    
    def position(self) -> XYpair:
        return self.walker.position
    
    def heading(self) -> Heading:
        return self.walker.heading
    
    def turn_at_intersection(self) -> None:
        self.walker.turn(next(self.turn_iter))
    
    def __lt__(self, other) -> bool:
        return self.position()[::-1] < other.position()[::-1]


class Mine(Space):
    def __init__(self, in_put) -> None:
        super().__init__(in_put, default=' ')
        
        self.carts: list[Cart] = []
        self.collisions: list[XYpair] = []
        for direction in '^v<>':
            if direction in self.items:
                self.carts.extend(Cart(pt, direction) for pt in self.items[direction])
                if direction in '<>':
                    self.items['-'].update(self.items[direction])
                else:
                    self.items['|'].update(self.items[direction])
                del self.items[direction]
    
    def tick(self) -> None:
        carts_to_remove: list[Cart] = []
        cart_locations: set[XYpair] = {c.position() for c in self.carts}
        for cart in sorted(self.carts):
            if cart in carts_to_remove:
                continue
            
            cart_locations.remove(cart.position())
            cart.walker.step()
            if cart.position() in cart_locations:
                self.collisions.append(cart.position())
                carts_to_remove.extend(c for c in self.carts if c.position() == cart.position())
                cart_locations -= {c.position() for c in carts_to_remove}
                continue
            
            cart_locations.add(cart.position())
            if cart.position() in self.items['+']:
                cart.turn_at_intersection()
            elif cart.position() in self.items['\\']:
                if cart.heading().vertical():
                    cart.walker.turn('LEFT')
                else:
                    cart.walker.turn('RIGHT')
            elif cart.position() in self.items['/']:
                if cart.heading().horizontal():
                    cart.walker.turn('LEFT')
                else:
                    cart.walker.turn('RIGHT')
        
        for cart in carts_to_remove:
            self.carts.remove(cart)


def parse(puzzle_input: str):
    """Parse input"""
    return Mine(puzzle_input.replace('\t', ' ' * 4))


def part1(data):
    """Solve part 1"""
    while not data.collisions:
        data.tick()
    return data.collisions[0]


def part2(data):
    """Solve part 2"""
    while len(data.carts) > 1:
        data.tick()
    return data.carts.pop().position()


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = (7, 3)
    PART2_TEST_ANSWER = (6, 4)

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
