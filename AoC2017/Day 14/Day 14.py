import operator
import functools
from collections.abc import Set

from xypair import XYpair

PART1_TEST_ANSWER = 8108
PART2_TEST_ANSWER = 1242


def parse(puzzle_input: str):
    return puzzle_input.strip()


def knot_hash(input_str: str) -> int:
    lengths: list[int] = [ord(ch) for ch in input_str] + [17, 31, 73, 47, 23]
    list_size: int = 256
    rounds: int = 64

    # Create sparse hash
    cur_position: int = 0
    skip_size: int = 0
    sparse: list[int] = list(range(list_size))

    for _ in range(rounds):
        for length in lengths:
            if 0 < length < list_size:
                # Temporarily rotate list so current position is at head
                tmp_lst: list[int] = sparse[cur_position:] + sparse[:cur_position]

                # Reverse length
                tmp_lst = tmp_lst[length - 1::-1] + tmp_lst[length:]

                # Rotate list back to original position
                split_position: int = len(sparse) - cur_position
                sparse = tmp_lst[split_position:] + tmp_lst[:split_position]

            cur_position = (cur_position + length + skip_size) % len(sparse)
            skip_size += 1

    # Condense into dense hash
    block_size: int = 16
    dense: list[int] = []
    for i in range(0, len(sparse), block_size):
        dense.append(functools.reduce(operator.xor, sparse[i:i + block_size]))

    # Convert to hex string then integer
    return int(''.join(f'{n:02x}' for n in dense), 16)


def used_locations(input_key: str) -> set[XYpair]:
    used: set[XYpair] = set()
    for y in range(128):
        h: int = knot_hash(f'{input_key}-{y}')
        for x in range(128):
            if h & (1 << x):
                used.add(XYpair(x, y))
    return used


def on_disk(square: XYpair) -> bool:
    return 0 <= square.x < 128 and 0 <= square.y < 128


def expand_region(start: XYpair, used: Set[XYpair]) -> set[XYpair]:
    region: set[XYpair] = set()
    edge: set[XYpair] = {start}
    while edge:
        cur_square: XYpair = edge.pop()
        region.add(cur_square)
        neighbors: set[XYpair] = {n for n in cur_square.neighbors() if on_disk(n)} & used
        edge.update(neighbors - region)
    return region


def part1(data):
    return sum(knot_hash(f'{data}-{row}').bit_count() for row in range(128))


def part2(data):
    used: set[XYpair] = used_locations(data)
    num_regions: int = 0
    working: set[XYpair] = used.copy()
    while working:
        cur_square: XYpair = working.pop()
        working -= expand_region(cur_square, used)
        num_regions += 1
    return num_regions


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
