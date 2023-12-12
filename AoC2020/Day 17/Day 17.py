import pathlib
import sys
import os
from collections import namedtuple

Point3 = namedtuple('Point3', 'x y z')
Point4 = namedtuple('Point4', 'x y z w')


def parse(puzzle_input):
    """Parse input"""
    active_cubes: list[tuple[int, int]] = []
    for y, line in enumerate(puzzle_input.split('\n')):
        for x, cube in enumerate(line):
            if cube == '#':
                active_cubes.append((x, y))
    return active_cubes


class PocketDimension3:
    def __init__(self, active: list[tuple[int, int]]):
        self.active_cubes: set[Point3] = {Point3(x, y, 0) for x, y in active}

    @staticmethod
    def get_neighbors(cube: Point3) -> set[Point3]:
        neighbors: set[Point3] = set()
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    neighbors.add(Point3(cube.x + i, cube.y + j, cube.z + k))
        neighbors.remove(cube)
        return neighbors

    def update(self) -> None:
        cells_to_update: set[Point3] = set()
        for cube in self.active_cubes:
            cells_to_update.add(cube)
            cells_to_update.update(self.get_neighbors(cube))

        updated_cells: set[Point3] = set()
        for cube in cells_to_update:
            active_neighbors: int = len(self.active_cubes & self.get_neighbors(cube))
            if cube in self.active_cubes and active_neighbors in (2, 3):
                updated_cells.add(cube)
            elif cube not in self.active_cubes and active_neighbors == 3:
                updated_cells.add(cube)

        self.active_cubes = updated_cells

    def run(self, steps: int) -> None:
        for _ in range(steps):
            if not self.active_cubes:
                break
            self.update()


class PocketDimension4:
    def __init__(self, active: list[tuple[int, int]]):
        self.active_cubes: set[Point4] = {Point4(x, y, 0, 0) for x, y in active}

    @staticmethod
    def get_neighbors(cube: Point4) -> set[Point4]:
        neighbors: set[Point4] = set()
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    for m in (-1, 0, 1):
                        neighbors.add(Point4(cube.x + i, cube.y + j, cube.z + k, cube.w + m))
        neighbors.remove(cube)
        return neighbors

    def update(self) -> None:
        cells_to_update: set[Point4] = set()
        for cube in self.active_cubes:
            cells_to_update.add(cube)
            cells_to_update.update(self.get_neighbors(cube))

        updated_cells: set[Point4] = set()
        for cube in cells_to_update:
            active_neighbors: int = len(self.active_cubes & self.get_neighbors(cube))
            if cube in self.active_cubes and active_neighbors in (2, 3):
                updated_cells.add(cube)
            elif cube not in self.active_cubes and active_neighbors == 3:
                updated_cells.add(cube)

        self.active_cubes = updated_cells

    def run(self, steps: int) -> None:
        for _ in range(steps):
            if not self.active_cubes:
                break
            self.update()


def part1(data):
    """Solve part 1"""
    pd: PocketDimension3 = PocketDimension3(data)
    pd.run(6)
    return len(pd.active_cubes)


def part2(data):
    """Solve part 2"""
    pd: PocketDimension4 = PocketDimension4(data)
    pd.run(6)
    return len(pd.active_cubes)


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
