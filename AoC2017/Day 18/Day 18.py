import typing

from computer import AbstractComputer

PART1_TEST_ANSWER = 4
PART2_TEST_ANSWER = 3


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


class Computer(AbstractComputer):
    def operand_value(self, op: str) -> int:
        return self.register[op] if op.isalpha() else self.immediate_value(op)

    def decode(self) -> int:
        self.instruction = typing.cast(str, self.instruction)
        self.opcode, *operands = self.instruction.split()

        # --- part 2 only --- #
        if self.opcode == 'rcv' and not self.input_available():
            return self.WAIT_FOR_INPUT
        # ------------------- #

        match self.opcode:
            case 'add' | 'mul' | 'mod' | 'set':
                x, y = operands
                self.operands = (x, self.operand_value(y))
            case 'snd':
                x, = operands
                self.operands = (self.operand_value(x), )
            case 'rcv':
                x, = operands
                self.operands = (x, )
            case 'jgz':
                x, y = operands
                self.operands = (self.operand_value(x), self.operand_value(y))

        return self.SUCCESS

    def execute(self) -> None:
        match self.opcode:
            case 'add':
                x, y = self.operands
                self.register[x] += y
            case 'mul':
                x, y = self.operands
                self.register[x] *= y
            case 'mod':
                x, y = self.operands
                self.register[x] %= y
            case 'set':
                x, y = self.operands
                self.register[x] = y
            case 'snd':
                x, = self.operands  # noqa
                self.add_to_output_buffer(x)
            case 'rcv':
                x, = self.operands  # noqa

                # part 1
                """if x != 0:
                    while self.output_buffer_length() > 1:
                        self.next_output()
                    self.add_to_input_buffer([self.next_output()])"""

                # part 2
                self.register[x] = self.next_input()

            case 'jgz':
                x, y = self.operands
                if x > 0:
                    self.jump_relative(y)


def deadlock(cpu0: Computer, cpu1: Computer) -> bool:
    return not (cpu0.input_available() or cpu0.output_available() or
                cpu1.input_available() or cpu1.output_available())


def part1(data):
    cpu: Computer = Computer()
    cpu.load_memory(data)
    while not cpu.input_available():
        cpu.step()
    return cpu.next_input()


def part2(data):
    cpu0: Computer = Computer()
    cpu0.load_memory(data)
    cpu0.register['p'] = 0
    cpu0.run()

    cpu1: Computer = Computer()
    cpu1.load_memory(data)
    cpu1.register['p'] = 1
    cpu1.run()
    
    while not deadlock(cpu0, cpu1):
        cpu0.run()
        cpu0.send_to(cpu1)
        
        cpu1.run()
        cpu1.send_to(cpu0)
        
    return cpu1.outputs_generated


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

    # test(1, working_directory)
    test(2, working_directory)
    print()
    # solve(1, working_directory)
    solve(2, working_directory)
