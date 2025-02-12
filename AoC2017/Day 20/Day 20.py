import collections
import itertools

from xyztrio import XYZtrio, ORIGIN
from particle import Particle3D

PART1_TEST_ANSWER = 0
PART2_TEST_ANSWER = 1


def parse(puzzle_input: str):
    particles: list[Particle3D] = []
    for line in puzzle_input.split('\n'):
        p, v, a = line.split('>, ')
        position: XYZtrio = XYZtrio(*(int(n) for n in p.lstrip('p=<').split(',')))
        velocity: XYZtrio = XYZtrio(*(int(n) for n in v.lstrip('v=<').split(',')))
        acceleration: XYZtrio = XYZtrio(*(int(n) for n in a.lstrip('a=<').rstrip('>').split(',')))
        particles.append(Particle3D(position, velocity, acceleration))
    return particles


def part1(data):
    min_accel: int = min(data, key=lambda p: p.acceleration.manhattan_distance(ORIGIN))
    return data.index(min_accel)


def part2(data):  # 601 is too high
    particles_remaining: set[Particle3D] = set(data)
    collisions: list[tuple[int, Particle3D, Particle3D]] = []
    for p1, p2 in itertools.combinations(data, 2):
        if (t := p1.collision_time(p2)) != -1:
            collisions.append((t, p1, p2))

    collisions.sort()

    destroyed: dict[int, set[Particle3D]] = collections.defaultdict(set)
    for t, p1, p2 in collisions:
        if (p1 in particles_remaining and p2 in particles_remaining) or \
           (p1 in particles_remaining and p2 in destroyed[t]) or \
           (p2 in particles_remaining and p1 in destroyed[t]):

            destroyed[t].update((p1, p2))
            particles_remaining.difference_update((p1, p2))

    return len(particles_remaining)


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
