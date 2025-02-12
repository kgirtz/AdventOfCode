from collections.abc import Iterable

from xypair import XYpair, XYtuple, ORIGIN

PART1_TEST_ANSWER = 12  # 12
PART2_TEST_ANSWER = None


class Image:
    def __init__(self, size: int, pixels: Iterable[XYtuple], top_left: XYtuple = ORIGIN) -> None:
        self.position: XYpair = XYpair(*top_left)
        self.size: int = size
        self.active_pixels: set[XYpair] = {XYpair(*pixel) - self.position for pixel in pixels}

    def pixels(self) -> set[XYpair]:
        return {pixel + self.position for pixel in self.active_pixels}

    def enhance(self) -> None:
        if self.size % 2 == 0:
            for y in range(0, self.size, 2):
                for x in range(0, self.size, 2):
                    top_left: XYpair = XYpair(x, y)
                    sub_active: set[XYpair] = {top_left,        top_left.right(),
                                               top_left.down(), top_left.down_right()} & self.active_pixels
                    sub_image: Image = Image(2, sub_active, top_left)

        else:
            assert self.size % 3 == 0

            for y in range(0, self.size, 3):
                for x in range(0, self.size, 3):
                    top_left: XYpair = XYpair(x, y)
                    center: XYpair = top_left.down_right()
                    sub_active: set[XYpair] = {center.up_left(),   center.up(),   center.up_right(),
                                               center.left(),      center,        center.right(),
                                               center.down_left(), center.down(), center.down_right()} & self.active_pixels
                    sub_image: Image = Image(3, sub_active, top_left)


class Rule:
    def __init__(self, rule: str) -> None:
        before_str, after_str = rule.strip().split(' => ')
        before: list[str] = before_str.strip().split('/')
        after: list[str] = after_str.strip().split('/')

        self.size_before: int = len(before)
        self.on_before: set[XYpair] = set()
        for y in range(self.size_before):
            for x in range(self.size_before):
                if before[y][x] == '#':
                    self.on_before.add(XYpair(x, y))

        self.size_after: int = len(after)
        self.on_after: set[XYpair] = set()
        for y in range(self.size_after):
            for x in range(self.size_after):
                if after[y][x] == '#':
                    self.on_after.add(XYpair(x, y))

    def matches(self, image: Image) -> bool:
        ...


def parse(puzzle_input: str):
    return [Rule(line) for line in puzzle_input.split('\n')]


def part1(data):
    iterations: int = 2  # test = 2, input = 5
    image: Image = Image(3, ((1, 0), (2, 1), (0, 2), (1, 2), (2, 2)))
    for _ in range(iterations):
        image.enhance()
    return len(image.active_pixels)


def part2(data):
    return None


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
