
PART1_TEST_ANSWER = 3
PART2_TEST_ANSWER = 14


def parse(puzzle_input: str):
    fresh_str, available_str = puzzle_input.split('\n\n')

    fresh: list[tuple[int, int]] = []
    for id_range in fresh_str.split('\n'):
        ends: list[str] = id_range.split('-')
        fresh.append((int(ends[0]), int(ends[1])))

    available: list[int] = [int(aid) for aid in available_str.split('\n')]

    return fresh, available


def in_range(iid: int, id_range: tuple[int, int]) -> bool:
    return id_range[0] <= iid <= id_range[1]


def ranges_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    return r1[1] >= r2[0] and r1[0] <= r2[1]


def part1(data):
    fresh, available = data
    return sum(any(in_range(iid, id_range) for id_range in fresh) for iid in available)


def part2(data):
    fresh: set[tuple[int, int]] = set(data[0])

    # Merge overlapping ranges
    keep_merging: bool = True
    while keep_merging:
        keep_merging = False
        temp_merged: set[tuple[int, int]] = set()
        while fresh:
            a: tuple[int, int] = fresh.pop()
            for b in list(fresh):
                if ranges_overlap(a, b):
                    keep_merging = True
                    a = (min(a[0], b[0]), max(a[1], b[1]))
                    fresh.remove(b)
            temp_merged.add(a)
        fresh = temp_merged

    return sum((id_range[1] - id_range[0] + 1) for id_range in fresh)


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
