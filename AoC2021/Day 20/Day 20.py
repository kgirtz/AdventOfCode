import pathlib
import sys
import os
from typing import Optional


class Image:
    def __init__(self, pixel_matrix: list[list[str]]) -> None:
        self.background: str = '.'
        self.x_min: int = 0
        self.x_max: int = len(pixel_matrix[0]) - 1
        self.y_min: int = 0
        self.y_max: int = len(pixel_matrix) - 1
        self.pixels: dict[tuple[int, int], str] = {}
        for y in range(self.y_max + 1):
            for x in range(self.x_max + 1):
                self.pixels[(x, y)] = pixel_matrix[y][x]

    def __str__(self) -> str:
        im_str: str = ''
        for y in range(self.y_min, self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                im_str += self.pixels[(x, y)]
            im_str += '\n'
        return im_str


def parse(puzzle_input):
    """Parse input"""
    algorithm, pixels = puzzle_input.split('\n\n')
    image: Image = Image([list(line) for line in pixels.split('\n')])
    return algorithm, image


def pixels_to_num(pixels: str) -> int:
    return int(pixels.replace('.', '0').replace('#', '1'), 2)


def enhance_pixel(x: int, y: int, im: Image, alg: str) -> str:
    pixel_area: list[tuple[int, int]] = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                                         (x - 1, y), (x, y), (x + 1, y),
                                         (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    pixel_list: list[str] = [im.pixels.get(pt, im.background) for pt in pixel_area]
    enhancement_index: int = pixels_to_num(''.join(pixel_list))
    return alg[enhancement_index]


def enhance(im: Image, alg: str) -> None:
    enhanced_pixels: dict[tuple[int, int], str] = {}
    for x, y in im.pixels:
        enhanced_pixels[(x, y)] = enhance_pixel(x, y, im, alg)

    for x in range(im.x_min, im.x_max + 1):
        enhanced_pixels[(x, im.y_min - 1)] = enhance_pixel(x, im.y_min - 1, im, alg)
        enhanced_pixels[(x, im.y_max + 1)] = enhance_pixel(x, im.y_max + 1, im, alg)

    for y in range(im.y_min - 1, im.y_max + 2):
        enhanced_pixels[(im.x_min - 1, y)] = enhance_pixel(im.x_min - 1, y, im, alg)
        enhanced_pixels[(im.x_max + 1, y)] = enhance_pixel(im.x_max + 1, y, im, alg)

    im.pixels = enhanced_pixels
    im.x_min -= 1
    im.x_max += 1
    im.y_min -= 1
    im.y_max += 1
    if im.background == '.':
        im.background = alg[0]
    elif im.background == '#':
        im.background = alg[-1]


def lit_pixels(im: Image) -> Optional[int]:
    if im.background == '#':
        return None
    return list(im.pixels.values()).count('#')


def part1(data):
    """Solve part 1"""
    algorithm, image = data
    enhance(image, algorithm)
    enhance(image, algorithm)
    return lit_pixels(image)


def part2(data):
    """Solve part 2"""
    algorithm, image = data
    for _ in range(50):
        enhance(image, algorithm)
    return lit_pixels(image)


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
