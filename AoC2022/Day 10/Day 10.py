
from computer import AbstractComputer, SpecialRegister

PART1_TEST_ANSWER = 13140
PART2_TEST_ANSWER = '##..##..##..##..##..##..##..##..##..##..\n' + \
                    '###...###...###...###...###...###...###.\n' + \
                    '####....####....####....####....####....\n' + \
                    '#####.....#####.....#####.....#####.....\n' + \
                    '######......######......######......####\n' + \
                    '#######.......#######.......#######.....'


class CRT(AbstractComputer):
    CYCLES_PER_INSTRUCTION: dict[str, int] = {'addx': 2}

    IMAGE_WIDTH: int = 40
    IMAGE_HEIGHT: int = 6

    x: SpecialRegister = SpecialRegister()

    def __init__(self, max_cycles: int = -1) -> None:
        super().__init__()

        self.max_cycles: int = int(max_cycles)
        self.crt: list[str] = []

        self.reset()

    def reset(self) -> None:
        super().reset()

        self.x = 1
        self.crt = [''] * self.IMAGE_HEIGHT

    def step(self) -> bool:
        if 0 < self.max_cycles <= self.clock_cycles:
            return self.BREAK
        return super().step()

    def draw_pixel(self, cycle_count: int) -> None:
        x: int = cycle_count % self.IMAGE_WIDTH
        y: int = cycle_count // self.IMAGE_WIDTH
        self.crt[y] += '#' if abs(x - self.x) <= 1 else '.'

    def image(self) -> str:
        return '\n'.join(self.crt)

    def execute(self) -> int | None:
        # Draw pixel during first clock cycle no matter what
        self.draw_pixel(self.clock_cycles)

        match self.opcode:
            case 'noop':
                ...
            case 'addx':
                # Make sure multi-cycle instructions don't get executed past the limit
                if 0 < self.max_cycles <= self.clock_cycles + 1:
                    return self.HALT

                # Draw another pixel during second clock cycle
                self.draw_pixel(self.clock_cycles + 1)

                v, = self.operands
                self.x += v


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    crt: CRT = CRT()
    crt.load_memory(data)

    signal_strength: int = 0
    for cycle_count in range(20, 220 + 1, 40):
        crt.reset()
        crt.max_cycles = cycle_count - 1
        crt.run()
        signal_strength += crt.x * cycle_count
    return signal_strength


def part2(data):
    crt: CRT = CRT()
    crt.load_memory(data)
    crt.run()
    print('\n' + crt.image().replace('.', ' ') + '\n')
    return crt.image()


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
