import pathlib
import sys
import os
import parse as scanf
from math import lcm


def parse(puzzle_input):
    """Parse input"""
    positions: list[tuple] = []
    for line in puzzle_input.split('\n'):
        x, y, z = scanf.parse('<x={:d}, y={:d}, z={:d}>', line)
        positions.append((x, y, z))
    return positions


class Moon:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.v_x: int = 0
        self.v_y: int = 0
        self.v_z: int = 0

    def __str__(self) -> str:
        pos: str = f'x={self.x}, y={self.y}, z={self.z}'
        vel: str = f'x={self.v_x}, y={self.v_y}, z={self.v_z}'
        return f'pos=<{pos}>, vel=<{vel}>'

    def __eq__(self, other) -> bool:
        if (self.x, self.y, self.z) != (other.x, other.y, other.z):
            return False
        if (self.v_x, self.v_y, self.v_z) != (other.v_x, other.v_y, other.v_z):
            return False
        return True

    def potential_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self) -> int:
        return abs(self.v_x) + abs(self.v_y) + abs(self.v_z)

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

    def apply_gravity(self, g_x: int, g_y: int, g_z: int) -> None:
        self.v_x += g_x
        self.v_y += g_y
        self.v_z += g_z

    def apply_velocity(self) -> None:
        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z


def calculate_gravity(m0: Moon, m1: Moon, g0: list[int], g1: list[int]) -> None:
    if m0.x > m1.x:
        g0[0] -= 1
        g1[0] += 1
    elif m0.x < m1.x:
        g0[0] += 1
        g1[0] -= 1

    if m0.y > m1.y:
        g0[1] -= 1
        g1[1] += 1
    elif m0.y < m1.y:
        g0[1] += 1
        g1[1] -= 1

    if m0.z > m1.z:
        g0[2] -= 1
        g1[2] += 1
    elif m0.z < m1.z:
        g0[2] += 1
        g1[2] -= 1


def step(moons: list[Moon]) -> None:
    gravity_update: list[list[int]] = [[0, 0, 0] for _ in moons]
    for i, m0 in enumerate(moons):
        for j, m1 in enumerate(moons[i + 1:], i + 1):
            calculate_gravity(m0, m1, gravity_update[i], gravity_update[j])

    for i, moon in enumerate(moons):
        moon.apply_gravity(*gravity_update[i])
        moon.apply_velocity()


def states_equal(s1: list[Moon], s2: list[Moon]) -> bool:
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True


def partial_state(moons: list[Moon], dim: str) -> tuple[int, ...]:
    if dim == 'x':
        return tuple([m.x for m in moons] + [m.v_x for m in moons])
    if dim == 'y':
        return tuple([m.y for m in moons] + [m.v_y for m in moons])
    if dim == 'z':
        return tuple([m.z for m in moons] + [m.v_z for m in moons])


def periods(moons: list[Moon]) -> tuple[list[int], list[int]]:
    period: list[int] = [0, 0, 0]
    tail: list[int] = [0, 0, 0]

    x_visited: dict[tuple, int] = {partial_state(moons, 'x'): 0}
    y_visited: dict[tuple, int] = {partial_state(moons, 'y'): 0}
    z_visited: dict[tuple, int] = {partial_state(moons, 'z'): 0}

    steps: int = 0
    while 0 in period:
        step(moons)
        steps += 1

        if period[0] == 0:
            x_state: tuple[int, ...] = partial_state(moons, 'x')
            if x_state in x_visited:
                tail[0] = x_visited[x_state]
                period[0] = steps - tail[0]
            else:
                x_visited[x_state] = steps
        if period[1] == 0:
            y_state: tuple[int, ...] = partial_state(moons, 'y')
            if y_state in y_visited:
                tail[1] = y_visited[y_state]
                period[1] = steps - tail[1]
            else:
                y_visited[y_state] = steps
        if period[2] == 0:
            z_state: tuple[int, ...] = partial_state(moons, 'z')
            if z_state in z_visited:
                tail[2] = z_visited[z_state]
                period[2] = steps - tail[2]
            else:
                z_visited[z_state] = steps

    return period, tail


def part1(data):
    """Solve part 1"""
    moons: list[Moon] = [Moon(x, y, z) for x, y, z in data]
    for _ in range(1000):
        step(moons)
    return sum(moon.total_energy() for moon in moons)


def part2(data):
    """Solve part 2"""
    moons: list[Moon] = [Moon(x, y, z) for x, y, z in data]
    period, tail = periods(moons)
    return lcm(*period) + max(tail)


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
