import typing
from collections.abc import Sequence

from computer import AbstractComputer

PART1_TEST_ANSWER = None
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


class Computer(AbstractComputer):
    def operand_value(self, op: str) -> int:
        return self.register[op] if op.isalpha() else self.immediate_value(op)

    def decode(self) -> int:
        self.instruction = typing.cast(str, self.instruction)
        self.opcode, *operands = self.instruction.split()

        x, y = operands
        if self.opcode == 'jnz':
            x = self.operand_value(x)
        y = self.operand_value(y)

        self.operands = (x, y)

        return self.SUCCESS

    def execute(self) -> None:
        match self.opcode:
            case 'sub':
                x, y = self.operands
                self.register[x] -= y
            case 'mul':
                x, y = self.operands
                self.register[x] *= y
            case 'set':
                x, y = self.operands
                self.register[x] = y
            case 'jnz':
                x, y = self.operands
                if x != 0:
                    self.jump_relative(y)
    
    def decompile(self, program: Sequence[str]) -> str:
        instructions: list[str] = []
        for address, instruction in enumerate(program):
            line: str = self.analyze(instruction)
            instructions.append(f'{address}: ' + line + ('\n' if 'jmp' in line else ''))
        
        return '\n'.join(instructions)

    @staticmethod
    def analyze(instruction: str) -> str:
        mnemonic, x, y = instruction.split()
        if y.isalpha():
            y = f'r[{y}]'

        match mnemonic:
            case 'sub':
                if y.startswith('-'):
                    return f'r[{x}] += {y.lstrip("-")}'
                return f'r[{x}] -= {y}'
            case 'mul':
                return f'r[{x}] *= {y}'
            case 'set':
                return f'r[{x}] = {y}'
            case 'jnz':
                return f'if ({x} != 0): jmp {y}'
            case _:
                return ''


def part1(data):
    cpu: Computer = Computer()
    cpu.load_memory(data)
    cpu.run()
    return cpu.instruction_count['mul']


def part2(data):
    cpu: Computer = Computer()
    
    # print(cpu.decompile(data))
    
    # From program reverse engineering
    for b in range(109900, 126900 + 1, 17):
        if b % 2 == 0:
            cpu.register['h'] += 1
            continue
        for d in range(3, b, 2):
            if b % d == 0:
                cpu.register['h'] += 1
                break
    
    cpu.register['a'] = 1
    # cpu.run(data)  # Takes a long time, but should HALT
    
    return cpu.register['h']


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
