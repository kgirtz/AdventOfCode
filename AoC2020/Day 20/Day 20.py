import pathlib
import sys
import os
import parse as scanf
from collections import defaultdict, deque, namedtuple
from typing import Optional

Borders = dict[str, str]
Point = namedtuple('Point', 'x y')


def parse(puzzle_input):
    """Parse input"""
    tiles: dict[int, list[str]] = {}
    for tile_str in puzzle_input.split('\n\n'):
        tile_id, tile = scanf.parse('Tile {:d}:\n{}', tile_str)
        tiles[tile_id] = tile.split('\n')
    return tiles


class Tile:
    def __init__(self, tile_id: int, tile: list[str]) -> None:
        self.id: int = tile_id
        self.top: str = tile[0]
        self.bottom: str = tile[-1]
        self.left: str = ''.join(row[0] for row in tile)
        self.right: str = ''.join(row[-1] for row in tile)
        self.tile: list[str] = [row[1:-1] for row in tile[1:-1]]
        self.height: int = len(self.left)

    def rotate(self) -> None:
        self.tile = rotate_image(self.tile)
        self.top, self.right, self.bottom, self.left = self.left[::-1], self.top, self.right[::-1], self.bottom

    def flip(self) -> None:
        self.tile = self.tile[::-1]
        self.top, self.bottom = self.bottom, self.top
        self.left = self.left[::-1]
        self.right = self.right[::-1]

    def num_active_pixels(self) -> int:
        return sum(row.count('#') for row in self.tile)

    def aligned(self, borders: Borders) -> bool:
        if 'left' in borders and borders['left'] != self.left:
            return False
        if 'right' in borders and borders['right'] != self.right:
            return False
        if 'top' in borders and borders['top'] != self.top:
            return False
        if 'bottom' in borders and borders['bottom'] != self.bottom:
            return False
        return True


class Image:
    def __init__(self) -> None:
        self.image: dict[Point, Tile] = {}
        self.top: int = 0
        self.bottom: int = 0
        self.left: int = 0
        self.right: int = 0
        self.tile_height: int = 0
        self.surrounding: defaultdict[Point, Borders] = defaultdict(dict)

    def num_active_pixels(self) -> int:
        return sum(tile.num_active_pixels() for tile in self.image.values())

    def add_tile(self, tile: Tile, pos: Point) -> None:
        self.image[pos] = tile
        self.top = min(self.top, pos.y)
        self.bottom = max(self.bottom, pos.y)
        self.left = min(self.left, pos.x)
        self.right = max(self.right, pos.x)

        if pos in self.surrounding:
            del self.surrounding[pos]

        left: Point = Point(pos.x - 1, pos.y)
        if left not in self.image:
            self.surrounding[left]['right'] = tile.left

        right: Point = Point(pos.x + 1, pos.y)
        if right not in self.image:
            self.surrounding[right]['left'] = tile.right

        top: Point = Point(pos.x, pos.y - 1)
        if top not in self.image:
            self.surrounding[top]['bottom'] = tile.top

        bottom: Point = Point(pos.x, pos.y + 1)
        if bottom not in self.image:
            self.surrounding[bottom]['top'] = tile.bottom

    def corners(self) -> list[Point]:
        return [Point(self.left, self.top),
                Point(self.right, self.top),
                Point(self.left, self.bottom),
                Point(self.right, self.bottom)]

    def build_from_tiles(self, tiles: list[Tile]) -> None:
        self.tile_height = tiles[0].height - 2
        tiles: deque[Tile] = deque(tiles)
        origin: Point = Point(0, 0)
        self.add_tile(tiles.pop(), origin)

        while tiles:
            cur: Tile = tiles.popleft()
            target: Optional[Point] = matches_surrounding(cur, self.surrounding)
            if target:
                self.add_tile(cur, target)
            else:
                tiles.append(cur)

    def full_image(self) -> list[str]:
        compilation: list[str] = []
        for y in range(self.top, self.bottom + 1):
            rows: list[str] = [''] * self.tile_height
            for x in range(self.left, self.right + 1):
                cur_tile: Tile = self.image[Point(x, y)]
                for i in range(self.tile_height):
                    rows[i] += cur_tile.tile[i]
            compilation.extend(rows)
        return compilation


def rotate_image(image: list[str]) -> list[str]:
    new_image: list[str] = []
    for x in range(len(image[0])):
        new_image.append(''.join(row[x] for row in image[::-1]))
    return new_image


def sub_image_at_location(sub_image: list[str], x: int, y: int, image: list[str]) -> bool:
    for j in range(len(sub_image)):
        for i in range(len(sub_image[0])):
            if sub_image[j][i] == '#' and image[y + j][x + i] != '#':
                return False
    return True


def count_occurrences(sub_image: list[str], image: list[str]) -> int:
    occurrences: int = 0
    for y in range(len(image) - len(sub_image) + 1):
        for x in range(len(image[0]) - len(sub_image[0]) + 1):
            if sub_image_at_location(sub_image, x, y, image):
                occurrences += 1
    return occurrences


def matches_surrounding(tile: Tile, surrounding: defaultdict[Point, Borders]) -> Optional[Point]:
    for pos, borders in surrounding.items():
        for _ in range(2):
            if tile.aligned(borders):
                return pos
            for _ in range(3):
                tile.rotate()
                if tile.aligned(borders):
                    return pos
            tile.flip()
    return None


def part1(data):
    """Solve part 1"""
    tile_list: list[Tile] = [Tile(tile_id, pixels) for tile_id, pixels in data.held_items()]
    image: Image = Image()
    image.build_from_tiles(tile_list)

    product: int = 1
    for pt in image.corners():
        product *= image.image[pt].id
    return product


def part2(data):
    """Solve part 2"""
    tile_list: list[Tile] = [Tile(tile_id, pixels) for tile_id, pixels in data.held_items()]
    image: Image = Image()
    image.build_from_tiles(tile_list)
    total_pixels: int = image.num_active_pixels()
    full_image: list[str] = image.full_image()

    sea_monster: list[str] = ['                  # ',
                              '#    ##    ##    ###',
                              ' #  #  #  #  #  #   ']
    num_monster_pixels: int = sum(row.count('#') for row in sea_monster)

    for _ in range(2):
        num_sea_monsters: int = count_occurrences(sea_monster, full_image)
        if num_sea_monsters > 0:
            return total_pixels - num_monster_pixels * num_sea_monsters
        for _ in range(3):
            sea_monster = rotate_image(sea_monster)
            num_sea_monsters: int = count_occurrences(sea_monster, full_image)
            if num_sea_monsters > 0:
                return total_pixels - num_monster_pixels * num_sea_monsters
        sea_monster = sea_monster[::-1]


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
