import operator
import functools
from collections.abc import Iterable, Sequence

PART1_TEST_ANSWER = None  # 12
PART2_TEST_ANSWER = None


def parse(puzzle_input: str):
    return puzzle_input.strip()


def knot_hash(lengths: Iterable[int], list_size: int, rounds: int = 1) -> list[int]:
    cur_position: int = 0
    skip_size: int = 0
    lst: list[int] = list(range(list_size))
    
    for _ in range(rounds):
        for length in lengths:
            if 0 < length < list_size:
                # Temporarily rotate list so current position is at head
                tmp_lst: list[int] = lst[cur_position:] + lst[:cur_position]
                
                # Reverse length
                tmp_lst = tmp_lst[length - 1::-1] + tmp_lst[length:]
                
                # Rotate list back to original position
                split_position: int = len(lst) - cur_position
                lst = tmp_lst[split_position:] + tmp_lst[:split_position]
            
            cur_position = (cur_position + length + skip_size) % len(lst)
            skip_size += 1
    
    return lst


def condense(sparse_hash: Sequence[int]) -> list[int]:
    assert len(sparse_hash) == 256
    
    block_size: int = 16
    dense_hash: list[int] = []
    for i in range(0, len(sparse_hash), block_size):
        dense_hash.append(functools.reduce(operator.xor, sparse_hash[i:i + block_size]))
    return dense_hash


def part1(data):
    lengths: list[int] = [int(n) for n in data.split(',')]
    sparse_hash: Sequence[int] = knot_hash(lengths, 256)  # test = 5, input = 256
    return sparse_hash[0] * sparse_hash[1]


def part2(data):
    lengths: list[int] = [ord(ch) for ch in data] + [17, 31, 73, 47, 23]
    sparse_hash: Sequence[int] = knot_hash(lengths, 256, rounds=64)
    dense_hash: Iterable[int] = condense(sparse_hash)
    hex_hash: str = ''.join(f'{n:02x}' for n in dense_hash)
    return hex_hash


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
