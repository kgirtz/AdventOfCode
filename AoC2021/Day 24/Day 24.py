
PART1_TEST_ANSWER = None
PART2_TEST_ANSWER = None


class ALU:
    def __init__(self) -> None:
        self.var: dict[str, int] = {reg: 0 for reg in 'wxyz'}

    def __str__(self) -> str:
        return str(self.var)

    def run(self, program: list[str], input_str: str = '') -> None:
        for instruction in program:
            input_str = self.execute(instruction, input_str)

    def execute(self, instruction: str, input_str: str = '') -> str:
        if instruction.startswith('inp'):
            dst: str = instruction[-1]
            self.var[dst] = int(input_str[0])
            return input_str[1:]

        mnemonic, dst, op_str = instruction.split()
        if op_str[-1].isdigit():
            op = int(op_str)
        else:
            op = self.var[op_str]

        if mnemonic == 'add':
            self.var[dst] += op
        elif mnemonic == 'mul':
            self.var[dst] *= op
        elif mnemonic == 'div':
            self.var[dst] //= op
        elif mnemonic == 'mod':
            self.var[dst] %= op
        elif mnemonic == 'eql':
            self.var[dst] = int(self.var[dst] == op)

        return input_str


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    monad = data
    unit: ALU = ALU()
    for d1 in range(8, 0, -1):  # 1:8
        for d2 in range(9, 6, -1):  # 7:9
            for d3 in range(9, 0, -1):  # 1:9
                for d4 in range(5, 0, -1):  # 1:5
                    for d5 in range(9, 4, -1):  # 5:9
                        for d6 in range(7, 0, -1):  # 1:7
                            for d7 in range(9, 2, -1):  # 3:9
                                for d8 in range(4, 0, -1):  # 1:4
                                    for d9 in range(9, 8, -1):  # 9
                                        for d10 in range(1, 0, -1):  # 1
                                            for d11 in range(9, 5, -1):  # 6:9
                                                for d12 in range(9, 0, -1):  # 1:9
                                                    for d13 in range(3, 0, -1):  # 1:3
                                                        for d14 in range(9, 1, -1):  # 2:9
                                                            model_num: str = ''.join(str(d) for d in [d1, d2, d3, d4,
                                                                                                      d5, d6, d7, d8,
                                                                                                      d9, d10, d11, d12,
                                                                                                      d13, d14])
                                                            unit.run(monad, model_num)
                                                            if unit.var['z'] == 0:
                                                                return int(model_num)


def part2(data):
    monad = data
    unit: ALU = ALU()
    for d1 in range(1, 9):  # 1:8
        for d2 in range(7, 10):  # 7:9
            for d3 in range(1, 10):  # 1:9
                for d4 in range(1, 6):  # 1:5
                    for d5 in range(5, 10):  # 5:9
                        for d6 in range(1, 8):  # 1:7
                            for d7 in range(3, 10):  # 3:9
                                for d8 in range(1, 5):  # 1:4
                                    for d9 in range(9, 10):  # 9
                                        for d10 in range(1, 2):  # 1
                                            for d11 in range(6, 10):  # 6:9
                                                for d12 in range(1, 10):  # 1:9
                                                    for d13 in range(1, 4):  # 1:3
                                                        for d14 in range(2, 10):  # 2:9
                                                            model_num: str = ''.join(str(d) for d in [d1, d2, d3, d4,
                                                                                                      d5, d6, d7, d8,
                                                                                                      d9, d10, d11, d12,
                                                                                                      d13, d14])
                                                            unit.run(monad, model_num)
                                                            if unit.var['z'] == 0:
                                                                return int(model_num)


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
