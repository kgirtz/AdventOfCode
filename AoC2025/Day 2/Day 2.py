
PART1_TEST_ANSWER = 1227775554
PART2_TEST_ANSWER = 4174379265


def parse(puzzle_input: str):
    ranges: list[tuple[int, int]] = []
    for r in puzzle_input.split(','):
        r = r.split('-')
        ranges.append((int(r[0]), int(r[1])))
    return ranges


def is_invalid(id_: int | str) -> bool:
    id_ = str(id_)
    if len(id_) % 2 == 1:
        return False

    middle: int = len(id_) // 2
    return id_[:middle] == id_[middle:]


def is_invalid_2(id_: int | str) -> bool:
    id_ = str(id_)
    middle: int = len(id_) // 2

    return any(id_ == id_[:sub_len] * (len(id_) // sub_len)
               for sub_len in range(1, middle + 1))


def part1(data):
    invalid_sum: int = 0
    for first, last in data:
        for i in range(first, last + 1):
            if is_invalid(i):
                invalid_sum += i

    return invalid_sum


def part2(data):
    invalid_sum: int = 0
    for first, last in data:
        for i in range(first, last + 1):
            if is_invalid_2(i):
                invalid_sum += i

    return invalid_sum


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
