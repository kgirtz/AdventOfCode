import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    passports: list[dict[str, str]] = []
    for passport_str in puzzle_input.split('\n\n'):
        passport: dict[str, str] = {}
        for passport_field in passport_str.split():
            field, value = passport_field.split(':')
            passport[field] = value
        passports.append(passport)
    return passports


def valid_field_count(passport: dict[str, str]) -> bool:
    if len(passport) < 7:
        return False
    if len(passport) == 7 and 'cid' in passport:
        return False
    return True


def valid_field_values(passport: dict[str, str]) -> bool:
    if not valid_field_count(passport):
        return False

    birth_year: int = int(passport['byr'])
    if birth_year < 1920 or birth_year > 2002:
        return False

    issue_year: int = int(passport['iyr'])
    if issue_year < 2010 or issue_year > 2020:
        return False

    exp_year: int = int(passport['eyr'])
    if exp_year < 2020 or exp_year > 2030:
        return False

    height: str = passport['hgt']
    if height.endswith('in'):
        inches: int = int(height[:-2])
        if inches < 59 or inches > 76:
            return False
    elif height.endswith('cm'):
        centimeters: int = int(height[:-2])
        if centimeters < 150 or centimeters > 193:
            return False
    else:
        return False

    hair_color: str = passport['hcl']
    if len(hair_color) != 7 or not hair_color.startswith('#'):
        return False
    for ch in hair_color[1:]:
        if not ch.isdigit() and ch not in 'abcdef':
            return False

    eye_color: str = passport['ecl']
    if eye_color not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
        return False

    passport_id: str = passport['pid']
    if len(passport_id) != 9 or not all(ch.isdigit() for ch in passport_id):
        return False

    return True


def part1(data):
    """Solve part 1"""
    num_valid: int = 0
    for passport in data:
        if valid_field_count(passport):
            num_valid += 1
    return num_valid


def part2(data):
    """Solve part 2"""
    num_valid: int = 0
    for passport in data:
        if valid_field_values(passport):
            num_valid += 1
    return num_valid


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
