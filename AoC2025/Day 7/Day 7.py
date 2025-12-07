import collections.abc

from space import Space
from xypair import XYpair

PART1_TEST_ANSWER = 21
PART2_TEST_ANSWER = 40


class TachyonManifold(Space):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.entry: XYpair = self.items['S'].pop()
        self.splitters: set[XYpair] = self.items['^']

    def count_splits(self, beams: collections.abc.Iterable[XYpair]) -> int:
        return sum((beam.down() in self.splitters) for beam in beams)

    def propagate_downward(self, beams: collections.abc.Iterable[XYpair]) -> set[XYpair]:
        new_beams: set[XYpair] = set()
        for beam in beams:
            if beam.down() in self.splitters:
                new_beams |= {beam.down_left(), beam.down_right()}
            else:
                new_beams.add(beam.down())
        return new_beams


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    diagram: TachyonManifold = TachyonManifold(data)

    split_count: int = 0
    beams: set[XYpair] = {diagram.entry}
    for _ in range(diagram.height - 1):
        split_count += diagram.count_splits(beams)
        beams = diagram.propagate_downward(beams)

    return split_count


def part2(data):
    diagram: TachyonManifold = TachyonManifold(data)

    beams: dict[XYpair, int] = {diagram.entry: 1}
    for _ in range(diagram.height - 1):
        new_beams: dict[XYpair, int] = {}
        for b in diagram.propagate_downward(beams.keys()):
            new_beams[b] = beams.get(b.up(), 0)
            if b.left() in diagram.splitters:
                new_beams[b] += beams.get(b.up_left(), 0)
            if b.right() in diagram.splitters:
                new_beams[b] += beams.get(b.up_right(), 0)
        beams = new_beams

    return sum(beams.values())


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
