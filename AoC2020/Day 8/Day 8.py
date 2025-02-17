
from computer import AbstractComputer

PART1_TEST_ANSWER = 5
PART2_TEST_ANSWER = 8


class GameConsole(AbstractComputer):
    @property
    def accumulator(self) -> int:
        return self.register['acc']

    @accumulator.setter
    def accumulator(self, value: int) -> None:
        self.register['acc'] = value

    def execute(self) -> None:
        op: int = self.operands[0]
        match self.opcode:
            case 'acc':
                self.accumulator += op
            case 'jmp':
                self.jump_relative(op)
            case 'nop':
                ...

    def step(self) -> bool:
        # Console can never loop
        if self.ip in self.addresses_executed:
            return self.BREAK
        return super().step()


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    """Solve part 1"""
    console: GameConsole = GameConsole()
    console.load_memory(data)
    console.run()
    return console.accumulator


def part2(data):
    """Solve part 2"""
    console: GameConsole = GameConsole()

    program: list[str] = list(data)
    for address, instruction in enumerate(program):
        if 'nop' in instruction:
            program[address] = instruction.replace('nop', 'jmp')
        elif 'jmp' in instruction:
            program[address] = instruction.replace('jmp', 'nop')

        console.load_memory(program)
        console.run()
        if console.ip == len(program):
            return console.accumulator

        program[address] = instruction
        console.reset()


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
