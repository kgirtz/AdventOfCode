import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    return [tuple(line) for line in puzzle_input.split('\n')]


def mcb(nums: list[tuple], i: int) -> str:
    bit_sum: int = sum(int(num[i]) for num in nums)
    if bit_sum >= len(nums) / 2:
        return '1'
    return '0'


def part1(data):
    """Solve part 1"""
    binary_len: int = len(data[0])
    gamma: str = ''
    epsilon: str = ''
    for i in range(binary_len):
        most_common: str = mcb(data, i)
        gamma += most_common
        epsilon += '1' if most_common == '0' else '0'

    gamma_rate: int = int(gamma, 2)
    epsilon_rate: int = int(epsilon, 2)
    return gamma_rate * epsilon_rate


def part2(data):
    """Solve part 2"""
    binary_len: int = len(data[0])

    oxygen: list[tuple] = data.copy()
    for i in range(binary_len):
        most_common: str = mcb(oxygen, i)
        oxygen = [o for o in oxygen if o[i] == most_common]
        if len(oxygen) == 1:
            break

    co2: list[tuple] = data.copy()
    for i in range(binary_len):
        most_common: str = mcb(co2, i)
        co2 = [o for o in co2 if o[i] != most_common]
        if len(co2) == 1:
            break

    oxygen_generator_rating: int = int(''.join(oxygen[0]), 2)
    co2_scrubber_rating: int = int(''.join(co2[0]), 2)
    return oxygen_generator_rating * co2_scrubber_rating


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
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
