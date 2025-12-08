import heapq
import itertools
import typing
from collections.abc import Sequence, MutableSequence, Container, Iterable

from xyztrio import XYZtrio


PART1_TEST_ANSWER = None  # 40
PART2_TEST_ANSWER = 25272


XYZPairHeap: typing.TypeAlias = list[tuple[float, XYZtrio, XYZtrio]]


def parse(puzzle_input: str):
    trios: list[XYZtrio] = []
    for line in puzzle_input.split('\n'):
        x, y, z = [int(c) for c in line.split(',')]
        trios.append(XYZtrio(x, y, z))
    return trios


def build_distance_heap(boxes: Iterable[XYZtrio]) -> XYZPairHeap:
    distance_heap: XYZPairHeap = []
    for box1, box2 in itertools.combinations(boxes, 2):
        heapq.heappush(distance_heap, (box1.distance(box2), box1, box2))
    return distance_heap


def circuit_num(box: XYZtrio, circuits: Sequence[Container[XYZtrio]]) -> int:
    for i, circuit in enumerate(circuits):
        if box in circuit:
            return i
    return -1


def connect_boxes(box1: XYZtrio, box2: XYZtrio, circuits: MutableSequence[set[XYZtrio]]) -> None:
    connection: set[XYZtrio] = {box1, box2}

    num1: int = circuit_num(box1, circuits)
    num2: int = circuit_num(box2, circuits)

    if num1 == num2 == -1:  # Neither found
        circuits.append(connection)
    elif num1 == num2:  # Both found in same circuit
        circuits[num1].update(connection)
    elif num1 == -1:  # Only found box2
        circuits[num2].add(box1)
    elif num2 == -1:  # Only found box1
        circuits[num1].add(box2)
    else:  # Both found in different circuits
        circuits[num1].update(circuits[num2])
        circuits.pop(num2)


def part1(data):
    max_connections: int = 1000  # test = 10, input = 1000

    distance_heap: XYZPairHeap = build_distance_heap(data)

    circuits: list[set[XYZtrio]] = []
    for _ in range(max_connections):
        _, box1, box2 = heapq.heappop(distance_heap)
        connect_boxes(box1, box2, circuits)

    sizes: list[int] = sorted((len(circuit) for circuit in circuits), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def part2(data):
    distance_heap: XYZPairHeap = build_distance_heap(data)

    box1, box2 = None, None  # Avoid 'uninitialized' warning

    circuits: list[set[XYZtrio]] = []
    while not circuits or len(circuits[0]) < len(data):
        _, box1, box2 = heapq.heappop(distance_heap)
        connect_boxes(box1, box2, circuits)

    return box1.x * box2.x


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
