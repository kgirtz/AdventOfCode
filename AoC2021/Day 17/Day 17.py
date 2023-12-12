import pathlib
import sys
import os
import parse as scanf
from collections import namedtuple

PosVel = namedtuple('PosVel', 'x y Vx Vy')


def parse(puzzle_input):
    """Parse input"""
    return tuple(scanf.parse('target area: x={:d}..{:d}, y={:d}..{:d}', puzzle_input))


def step_x(pv: PosVel) -> PosVel:
    if pv.Vx < 0:
        return PosVel(pv.x + pv.Vx, pv.y, pv.Vx + 1, pv.Vy)
    elif pv.Vx > 0:
        return PosVel(pv.x + pv.Vx, pv.y, pv.Vx - 1, pv.Vy)
    else:
        return PosVel(pv.x + pv.Vx, pv.y, pv.Vx, pv.Vy)


def step_y(pv: PosVel) -> PosVel:
    return PosVel(pv.x, pv.y + pv.Vy, pv.Vx, pv.Vy - 1)


def step(pv: PosVel) -> PosVel:
    return step_y(step_x(pv))


def max_height(vy: int) -> int:
    last_y: int = -1
    cur_pv: PosVel = PosVel(0, 0, 0, vy)
    while cur_pv.y != last_y:
        last_y = cur_pv.y
        cur_pv = step_y(cur_pv)
    return last_y


def hits_target(vx: int, vy: int, left: int, right: int, low: int, high: int) -> bool:
    cur_pv: PosVel = PosVel(0, 0, vx, vy)
    while cur_pv.x <= right and cur_pv.y >= low:
        cur_pv = step(cur_pv)
        if left <= cur_pv.x <= right and low <= cur_pv.y <= high:
            return True
    return False


def min_x_velocity(target: int) -> int:
    for vx in range(2, target):
        cur_pv: PosVel = PosVel(0, 0, vx, 0)
        while True:
            if cur_pv.x >= target:
                return vx
            if cur_pv.Vx == 0:
                break
            cur_pv = step_x(cur_pv)


def max_y_velocity(top: int, bottom: int) -> int:
    return -bottom - 1


def part1(data):
    """Solve part 1"""
    left, right, bottom, top = data
    return max_height(max_y_velocity(top, bottom))


def part2(data):
    """Solve part 2"""
    left, right, bottom, top = data
    hits: set[tuple[int, int]] = set()
    for x in range(left, right + 1):
        for y in range(bottom, top + 1):
            hits.add((x, y))

    min_x: int = min_x_velocity(left)
    max_x: int = right // 2
    min_y: int = bottom // 2 + 1
    max_y: int = max_y_velocity(top, bottom)
    for vy in range(min_y, max_y + 1):
        for vx in range(min_x, max_x + 1):
            if (vx, vy) not in hits and hits_target(vx, vy, left, right, bottom, top):
                hits.add((vx, vy))
    return len(hits)


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
