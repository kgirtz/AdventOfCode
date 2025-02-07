from space import Space
from xypair import XYpair
from pointwalker import PointWalker

PART1_TEST_ANSWER = 'ABCDEF'
PART2_TEST_ANSWER = 38


class RoutingDiagram(Space):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.path: set[XYpair] = set()
        for pts in self.items.values():
            self.path.update(pts)
        
        self.letters: dict[XYpair, str] = {}
        for symbol, pts in self.items.items():
            if symbol.isalpha():
                pt: XYpair = list(pts).pop()
                self.letters[pt] = symbol
        
        self.starting_point: XYpair = min(self.items['|'], key=lambda pt: pt.y).up()


def parse(puzzle_input: str):
    return puzzle_input


def follow_path(diagram: RoutingDiagram) -> (str, int):
    walker: PointWalker = PointWalker(diagram.starting_point, 'SOUTH')
    passed: str = ''
    while True:
        if walker.position in diagram.letters:
            passed += diagram.letters[walker.position]
        
        if walker.next() in diagram.path:
            ...
        elif walker.peek('LEFT') in diagram.path:
            walker.turn('LEFT')
        elif walker.peek('RIGHT') in diagram.path:
            walker.turn('RIGHT')
        else:
            break
        
        walker.step()
    
    return passed, walker.steps_taken


def part1(data):
    diagram: RoutingDiagram = RoutingDiagram(data, default=' ')
    letters, _ = follow_path(diagram)
    return letters


def part2(data):
    diagram: RoutingDiagram = RoutingDiagram(data, default=' ')
    _, num_steps = follow_path(diagram)
    return num_steps


# ------------- DO NOT MODIFY BELOW THIS LINE ------------- #


import pathlib


def get_puzzle_input(file: pathlib.Path) -> str:
    if not file.exists():
        return ''
    return file.read_text().strip('\n').replace('\t', ' ' * 4)


def execute(func, puzzle_input: str) -> (..., int):
    import time

    start: int = time.perf_counter_ns()
    result = func(parse(puzzle_input))
    execution_time_us: int = (time.perf_counter_ns() - start) // 1000
    return result, execution_time_us


def timestamp(execution_time_us: int) -> str:
    stamp: str = f'{round(execution_time_us / 1000000, 3)} s'
    if execution_time_us < 1000000:
        stamp = f'{round(execution_time_us / 1000, 3)} ms'
    return f'\t[{stamp}]'


def test(part_num: int, directory: str) -> None:
    if part_num == 1:
        func = part1
        answer = PART1_TEST_ANSWER
    else:
        func = part2
        answer = PART2_TEST_ANSWER

    prefix: str = f'PART {part_num} TEST: '
    if answer is None:
        print(prefix + 'skipped')
        return

    file: pathlib.Path = pathlib.Path(directory, f'part{part_num}_test.txt')
    if not file.exists():
        file = pathlib.Path(directory, 'test.txt')

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    result = 'PASS' if result == answer else 'FAIL'
    print(prefix + result + timestamp(duration))


def solve(part_num: int, directory: str) -> None:
    func = part1 if part_num == 1 else part2
    prefix: str = f'PART {part_num}: '

    file: pathlib.Path = pathlib.Path(directory, 'input.txt')
    if not file.exists():
        # Download file?
        ...

    puzzle_input: str = get_puzzle_input(file)
    if not puzzle_input:
        print(prefix + 'no input')
        return

    result, duration = execute(func, puzzle_input)
    suffix: str = '' if result is None else timestamp(duration)
    print(prefix + str(result) + suffix)


if __name__ == '__main__':
    import os

    working_directory: str = os.path.dirname(__file__)

    test(1, working_directory)
    test(2, working_directory)
    print()
    solve(1, working_directory)
    solve(2, working_directory)
