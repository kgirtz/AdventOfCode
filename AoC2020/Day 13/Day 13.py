import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    lines: list[str] = puzzle_input.split('\n')
    earliest: int = int(lines[0])
    buses: list[str] = lines[1].split(',')
    return earliest, buses


def bus_nums(bus_list: list[str]) -> set[int]:
    return {int(bid) for bid in bus_list if bid != 'x'}


def get_offsets(ids: list[str]) -> list[tuple[int, int]]:
    offsets: list[tuple[int, int]] = []
    for i, bid in enumerate(ids):
        if bid != 'x':
            offsets.append((int(bid), i))
    return offsets


def valid(timestamp: int, requirements: list[tuple[int, int]]) -> bool:
    for bus_id, offset in requirements:
        if (timestamp + offset) % bus_id != 0:
            return False
    return True


def part1(data):
    """Solve part 1"""
    earliest, bus_list = data
    bus_ids: set[int] = bus_nums(bus_list)
    earliest_time: int = 2 * earliest
    earliest_bus: int = 0
    for bus in bus_ids:
        next_departure: int = earliest - (earliest % bus) + bus
        if next_departure < earliest_time:
            earliest_time = next_departure
            earliest_bus = bus
    return earliest_bus * (earliest_time - earliest)


def part2(data):
    """Solve part 2"""
    _, bus_list = data
    offsets: list[tuple[int, int]] = get_offsets(bus_list)

    step, _ = offsets[0]
    start: int = step
    for bus_id, offset in offsets[1:-1]:
        time: int = start
        while not valid(time, [(bus_id, offset)]):
            time += step
        start = time
        time += step
        while not valid(time, [(bus_id, offset)]):
            time += step
        step = time - start

    time = start
    while not valid(time, offsets):
        time += step

    return time


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
