import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [tuple(line.split(')')) for line in puzzle_input.split('\n')]


def satellite_map(orbit_list: list[tuple[str, str]]) -> dict[str, str]:
    satellite_of: dict[str, str] = {'COM': ''}
    for fixed, satellite in orbit_list:
        satellite_of[satellite] = fixed
    return satellite_of


def orbit_count(obj: str, satellite_of: dict[str, str], root: str = 'COM') -> int:
    orbits: int = 0
    cur: str = obj
    while cur != root:
        orbits += 1
        cur = satellite_of[cur]
    return orbits


def common_ancestor(sat1: str, sat2: str, satellite_of: dict[str, str]) -> str:
    sat1_ancestors: list[str] = [sat1]
    while sat1 != 'COM':
        sat1_ancestors.append(sat1)
        sat1 = satellite_of[sat1]

    sat2_ancestors: list[str] = [sat2]
    while sat2 != 'COM':
        sat2_ancestors.append(sat2)
        sat2 = satellite_of[sat2]

    common: str = sat1_ancestors[-1]
    while sat1_ancestors[-1] == sat2_ancestors[-1]:
        common = sat1_ancestors.pop()
        sat2_ancestors.pop()

    return common


def part1(data):
    """Solve part 1"""
    satellite_of: dict[str, str] = satellite_map(data)
    return sum(orbit_count(obj, satellite_of) for obj in satellite_of.keys())


def part2(data):
    """Solve part 2"""
    satellite_of: dict[str, str] = satellite_map(data)
    start: str = satellite_of['YOU']
    end: str = satellite_of['SAN']
    root: str = common_ancestor(start, end, satellite_of)
    return orbit_count(start, satellite_of, root) + orbit_count(end, satellite_of, root)


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
