import collections
from collections.abc import Sequence, Iterable
from typing import Self

PART1_TEST_ANSWER = 4
PART2_TEST_ANSWER = 3


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


class Computer:
    def __init__(self, program: Sequence[str]) -> None:
        self.registers: dict[str, int] = collections.defaultdict(int)
        self.ip: int = 0
        self.num_values_sent: int = 0
        self.send_buffer: collections.deque[int] = collections.deque()
        self.received_value: int | None = None
        self.program: list[str] = list(program)
        self.waiting_to_receive: bool = False
    
    def reset(self) -> None:
        self.registers.clear()
        self.ip = 0
        self.num_values_sent = 0
        self.send_buffer.clear()
        self.received_value = None
        self.waiting_to_receive = False

    def run(self, program: Sequence[int] = tuple()) -> None:
        if not program:
            program = self.program
        
        while 0 <= self.ip < len(program):
            instruction: str = program[self.ip]
            self.execute(instruction)
            self.ip += 1
            if self.waiting_to_receive:
                break
    
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
        match mnemonic:
            case 'add':
                x, y = operands
                self.registers[x] += self.operand_value(y)
            case 'mul':
                x, y = operands
                self.registers[x] *= self.operand_value(y)
            case 'mod':
                x, y = operands
                self.registers[x] %= self.operand_value(y)
            case 'set':
                x, y = operands
                self.registers[x] = self.operand_value(y)
            case 'snd':
                x, = operands
                self.send_buffer.append(self.operand_value(x))
            case 'rcv':
                x, = operands

                # part 1
                """if self.operand_value(x) != 0:
                    self.received_value = self.send_buffer[-1]"""

                # part 2
                self.waiting_to_receive = self.received_value is None
                if self.waiting_to_receive:
                    self.ip -= 1
                else:
                    self.registers[x] = self.received_value
                    self.received_value = None

            case 'jgz':
                x, y = operands
                if self.operand_value(x) > 0:
                    self.ip += self.operand_value(y) - 1
    
    def send_value(self, receiver: Self) -> None:
        if self.send_buffer:
            receiver.received_value = self.send_buffer.popleft()
            self.num_values_sent += 1


def deadlock(computers: Iterable[Computer]) -> bool:
    return all(cpu.waiting_to_receive and not cpu.send_buffer for cpu in computers)


def part1(data):
    cpu: Computer = Computer(data)
    while cpu.received_value is None:
        cpu.step()
    return cpu.received_value


def part2(data):
    cpu0: Computer = Computer(data)
    cpu1: Computer = Computer(data)
    cpu0.registers['p'] = 0
    cpu1.registers['p'] = 1
    
    while not deadlock((cpu0, cpu1)):
        cpu0.run()
        cpu0.send_value(cpu1)
        
        cpu1.run()
        cpu1.send_value(cpu0)
        
    return cpu1.num_values_sent


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

    #test(1, working_directory)
    test(2, working_directory)
    print()
    #solve(1, working_directory)
    solve(2, working_directory)
