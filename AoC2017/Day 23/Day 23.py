import collections
from collections.abc import Sequence, Iterable
from idlelib.mainmenu import menudefs

PART1_TEST_ANSWER = None
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


class Computer:
    def __init__(self, program: Iterable[str] = tuple()) -> None:
        self.registers: dict[str, int] = collections.defaultdict(int)
        self.ip: int = 0
        self.program: list[str] = list(program)
        self.instruction_counts: dict[str, int] = collections.defaultdict(int)
    
    def reset(self) -> None:
        self.registers.clear()
        self.ip = 0
        self.instruction_counts.clear()

    def run(self, program: Sequence[int] = tuple()) -> None:
        if not program:
            program = self.program
        
        while 0 <= self.ip < len(program):
            instruction: str = program[self.ip]
            self.execute(instruction)
            self.ip += 1
    
    def step(self) -> None:
        if not (0 <= self.ip < len(self.program)):
            raise IndexError('instruction pointer is outside program range')
        
        instruction: str = self.program[self.ip]
        self.execute(instruction)
        self.ip += 1
    
    def operand_value(self, operand: str) -> int:
        try:
            return int(operand)
        except ValueError:
            return self.registers[operand]

    def execute(self, instruction: str) -> None:
        mnemonic, *operands = instruction.split()
        self.instruction_counts[mnemonic] += 1

        match mnemonic:
            case 'sub':
                x, y = operands
                self.registers[x] -= self.operand_value(y)
            case 'mul':
                x, y = operands
                self.registers[x] *= self.operand_value(y)
            case 'set':
                x, y = operands
                self.registers[x] = self.operand_value(y)
            case 'jnz':
                x, y = operands
                if self.operand_value(x) != 0:
                    self.ip += self.operand_value(y) - 1
    
    def decompile(self, program: Sequence[str]) -> str:
        instructions: list[str] = []
        for address, instruction in enumerate(program):
            line: str = self.analyze(instruction, address)
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
    cpu.run(data)
    return cpu.instruction_counts['mul']


def part2(data):
    cpu: Computer = Computer()
    
    # print(cpu.decompile(data))
    
    # From program reverse engineering
    for b in range(109900, 126900 + 1, 17):
        if b % 2 == 0:
            cpu.registers['h'] += 1
            continue
        for d in range(3, b, 2):
            if b % d == 0:
                cpu.registers['h'] += 1
                break
    
    cpu.registers['a'] = 1
    # cpu.run(data)  # Takes a long time, but should HALT
    
    return cpu.registers['h']


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
