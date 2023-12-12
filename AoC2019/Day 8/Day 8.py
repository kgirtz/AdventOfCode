import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [int(n) for n in list(puzzle_input)]


def get_layers(image: list[int], height: int, width: int) -> list[list[int]]:
    area: int = height * width
    num_layers: int = len(image) // area

    return [image[area * i:area * (i + 1)] for i in range(num_layers)]


def build_image(layers: list[list[int]], height: int, width: int) -> list[int]:
    image: list[int] = []
    for i in range(height * width):
        for layer in layers:
            if layer[i] < 2:
                image.append(layer[i])
                break
    return image


def print_image(image: list[int], height: int, width: int) -> None:
    for row in range(height):
        for col in range(width):
            pixel = image[row * width + col]
            print('#' if pixel else ' ', end='')
        print()


def part1(data):
    """Solve part 1"""
    if len(data) < 50:
        height, width = 2, 3
    else:
        height, width = 6, 25

    layers: list[list[int]] = get_layers(data, height, width)
    fewest_zeros: list[int] = min(layers, key=lambda layer: layer.count(0))
    return fewest_zeros.count(1) * fewest_zeros.count(2)


def part2(data):
    """Solve part 2"""
    if len(data) < 20:
        height, width = 2, 2
    else:
        height, width = 6, 25

    layers: list[list[int]] = get_layers(data, height, width)
    image: list[int] = build_image(layers, height, width)
    print_image(image, height, width)


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
