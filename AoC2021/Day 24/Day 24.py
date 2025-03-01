import typing
from computer import AbstractComputer

PART1_TEST_ANSWER = None
PART2_TEST_ANSWER = None


class ALU(AbstractComputer):
    def decode(self) -> int | None:
        self.instruction = typing.cast(str, self.instruction)
        self.opcode, *operands = self.instruction.split()

        if self.opcode == 'inp':
            if not self.input_available():
                return self.HALT
            self.operands = operands
        else:
            a, b = operands
            self.operands = (a, self.register_or_immediate_operand_value(b))

    def execute(self) -> None:
        if self.opcode == 'inp':
            a, = self.operands
            self.register[a] = self.next_input()
        else:
            a, b = self.operands
            match self.opcode:
                case 'add':
                    self.register[a] += b
                case 'mul':
                    self.register[a] *= b
                case 'div':
                    self.register[a] //= b
                case 'mod':
                    self.register[a] %= b
                case 'eql':
                    self.register[a] = int(self.register[a] == b)


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    unit: ALU = ALU()
    unit.load_memory(data)
    for d1 in range(8, 0, -1):  # 1:8
        for d2 in range(9, 6, -1):  # 7:9
            for d3 in range(9, 0, -1):  # 1:9
                for d4 in range(5, 0, -1):  # 1:5
                    for d5 in range(9, 4, -1):  # 5:9
                        for d6 in range(7, 0, -1):  # 1:7
                            for d7 in range(9, 2, -1):  # 3:9
                                for d8 in range(4, 0, -1):  # 1:4
                                    for d11 in range(9, 5, -1):  # 6:9
                                        for d12 in range(9, 0, -1):  # 1:9
                                            for d13 in range(3, 0, -1):  # 1:3
                                                for d14 in range(9, 1, -1):  # 2:9
                                                    model_num: list[int] = [d1, d2, d3, d4, d5, d6, d7, d8,
                                                                            9, 1, d11, d12, d13, d14]
                                                    unit.reset()
                                                    unit.add_to_input_buffer(model_num)
                                                    unit.run()
                                                    if unit.register['z'] == 0:
                                                        return int(''.join(str(n) for n in model_num))


def part2(data):
    unit: ALU = ALU()
    unit.load_memory(data)
    for d1 in range(1, 9):  # 1:8
        for d2 in range(7, 10):  # 7:9
            for d3 in range(1, 10):  # 1:9
                for d4 in range(1, 6):  # 1:5
                    for d5 in range(5, 10):  # 5:9
                        for d6 in range(1, 8):  # 1:7
                            for d7 in range(3, 10):  # 3:9
                                for d8 in range(1, 5):  # 1:4
                                    for d11 in range(6, 10):  # 6:9
                                        for d12 in range(1, 10):  # 1:9
                                            for d13 in range(1, 4):  # 1:3
                                                for d14 in range(2, 10):  # 2:9
                                                    model_num: list[int] = [d1, d2, d3, d4, d5, d6, d7, d8,
                                                                            9, 1, d11, d12, d13, d14]
                                                    unit.reset()
                                                    unit.add_to_input_buffer(model_num)
                                                    unit.run()
                                                    if unit.register['z'] == 0:
                                                        return int(''.join(str(n) for n in model_num))


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
