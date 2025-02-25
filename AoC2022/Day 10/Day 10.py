

PART1_TEST_ANSWER = 13140
PART2_TEST_ANSWER = '##..##..##..##..##..##..##..##..##..##..\n' + \
                    '###...###...###...###...###...###...###.\n' + \
                    '####....####....####....####....####....\n' + \
                    '#####.....#####.....#####.....#####.....\n' + \
                    '######......######......######......####\n' + \
                    '#######.......#######.......#######.....\n'


def opcode(instruction: str) -> str:
    return instruction.split()[0]


def operand(instruction: str) -> str:
    match opcode(instruction):
        case 'noop':
            return ''
        case 'addx':
            return instruction.split()[1]


def execute_instruction(instruction: str, x: int) -> int:
    match opcode(instruction):
        case 'noop':
            return x
        case 'addx':
            return x + int(operand(instruction))


def expanded_program(program: list[str]) -> list[str]:
    # Replace addx(2-cyc) with noop/addx(1-cyc)
    for instruction in program:
        match opcode(instruction):
            case 'noop':
                yield 'noop'
            case 'addx':
                yield 'noop'
                yield instruction


def execute_program(program: list[str], max_cycles: int = 0) -> int:
    x: int = 1
    cycle_count: int = 0

    for instruction in expanded_program(program):
        x = execute_instruction(instruction, x)
        cycle_count += 1
        if cycle_count == max_cycles:
            break

    return x


def render_crt(program: list[str]) -> str:
    pixel_width: int = 40
    pixel_height: int = 6
    pixel_total: int = pixel_height * pixel_width

    crt: list[str] = ['' for _ in range(pixel_total)]

    x: int = 1
    cycle_count: int = 0

    for instruction in expanded_program(program):
        pixel_pos: int = cycle_count % pixel_width
        if abs(pixel_pos - x) <= 1:
            crt[cycle_count] = '#'
        else:
            crt[cycle_count] = '.'

        if (pixel_pos + 1) % pixel_width == 0:
            crt[cycle_count] += '\n'

        x = execute_instruction(instruction, x)
        cycle_count += 1
        if cycle_count == pixel_total:
            break

    return ''.join(crt)


def parse(puzzle_input: str):
    return puzzle_input.split('\n')


def part1(data):
    interesting_cycles: list[int] = list(range(20, 220 + 1, 40))

    signal_strengths: list[int] = [execute_program(data, c - 1) * c for c in interesting_cycles]

    return sum(signal_strengths)


def part2(data):
    image: str = render_crt(data)
    print('\n' + render_crt(data).replace('.', ' '))
    return image


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
