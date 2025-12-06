

PART1_TEST_ANSWER = 4277556
PART2_TEST_ANSWER = 3263827


def parse(puzzle_input: str):
    lines: list[str] = puzzle_input.split('\n')
    max_len: int = max(len(line) for line in lines)
    lines = [line + (' ' * (max_len - len(line))) for line in lines]
    return lines


def part1(data):
    numbers: list[list[int]] = [[int(n) for n in line.split()] for line in data[:-1]]
    operators: list[str] = data[-1].split()

    total: int = 0
    for i, op in enumerate(operators):
        if op == '+':
            total += sum(nums[i] for nums in numbers)
        elif op == '*':
            product: int = numbers[0][i]
            for nums in numbers[1:]:
                product *= nums[i]
            total += product

    return total


def part2(data):
    numbers: list[list[str]] = data[:-1]
    operators: list[str] = data[-1]

    total: int = 0
    pos: int = 0
    while pos < len(operators):
        op: str = operators[pos]
        next_space: int = pos + 1
        while next_space < len(operators) and (next_space + 1 == len(operators) or operators[next_space + 1] == ' '):
            next_space += 1

        nums: list[int] = []
        for i in range(pos, next_space):
            nums.append(int(''.join(num_line[i] for num_line in numbers)))

        if op == '+':
            total += sum(nums)
        elif op == '*':
            product: int = nums[0]
            for n in nums[1:]:
                product *= n
            total += product

        pos = next_space + 1

    return total


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
