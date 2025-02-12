from xypair import XYpair
from pointwalker import PointWalker
from space import Space

PART1_TEST_ANSWER = 5587
PART2_TEST_ANSWER = 2511944


class Cluster(Space):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.infected_nodes: set[XYpair] = self.items['#']
        self.weakened_nodes: set[XYpair] = set()
        self.flagged_nodes: set[XYpair] = set()
        self.carrier: PointWalker = PointWalker((self.width // 2, self.height // 2), 'NORTH')
        self.infections_caused: int = 0

    def burst(self, *, evolved: bool = False) -> None:
        cur_pos: XYpair = self.carrier.position
        if cur_pos in self.infected_nodes:
            self.carrier.turn('RIGHT')
            self.infected_nodes.remove(cur_pos)
            if evolved:
                self.flagged_nodes.add(cur_pos)

        elif cur_pos in self.weakened_nodes:
            self.weakened_nodes.remove(cur_pos)
            self.infected_nodes.add(cur_pos)
            self.infections_caused += 1

        elif cur_pos in self.flagged_nodes:
            self.carrier.turn('BACKWARD')
            self.flagged_nodes.remove(cur_pos)

        else:
            self.carrier.turn('LEFT')
            if evolved:
                self.weakened_nodes.add(cur_pos)
            else:
                self.infected_nodes.add(cur_pos)
                self.infections_caused += 1

        self.carrier.step()


def parse(puzzle_input: str):
    return puzzle_input.strip()


def part1(data):
    cluster: Cluster = Cluster(data)
    for _ in range(10000):
        cluster.burst()
    return cluster.infections_caused


def part2(data):
    cluster: Cluster = Cluster(data)
    for _ in range(10000000):
        cluster.burst(evolved=True)
    return cluster.infections_caused


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
    #solve(2, working_directory)
