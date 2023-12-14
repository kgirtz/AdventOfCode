import pathlib
import sys
import os
import re
import math
from typing import Sequence


def parse(puzzle_input):
    """Parse input"""
    data: list[tuple[list[str], list[int]]] = []
    for line in puzzle_input.split('\n'):
        springs, groups = line.split()
        data.append((springs, [int(g) for g in groups.split(',')]))
    return data


"""def possible_arrangements(springs: Sequence[str], groups: Sequence[int]) -> int:
    # Filter out definite matches or non-matches from beginning and end
    while groups:
        if len(springs[0]) < groups[0]:
            springs = springs[1:]
        elif len(springs[-1]) < groups[-1]:
            springs = springs[:-1]
        elif springs[0].startswith('#'):
            springs[0] = springs[0][groups[0]:]
            groups = groups[1:]
        elif springs[-1].endswith('#'):
            springs[-1] = springs[-1][:-groups[-1]]
            groups = groups[:-1]
        elif '#' * groups[0] in springs[0][:groups[0] + 1]:
            springs[0] = springs[0].lstrip('?')[groups[0]:]
            groups = groups[1:]
        elif '#' * groups[-1] in springs[-1][-2 * groups[-1]:]:
            springs[-1] = springs[-1].rstrip('?')[:-groups[-1]]
            groups = groups[:-1]
        else:
            break
        
        springs = ' '.join(springs).strip().split()
    
    if not groups:
        return 1
    
    # Filter out question marks that are too short to be a chunk
    springs = [s for s in springs if len(s) >= min(groups)]
    
    # Filter out separated question marks that can't be part of any chunk
    if len(springs) > len(groups):
        concrete_springs: list[str] = [s for s in springs if '#' in s]
        if len(concrete_springs) == len(groups):
            springs = concrete_springs

    if len(springs) == len(groups):
        arrangements: int = 1
        for spring, group in zip(springs, groups):
            if '#' in spring:
                first: int = spring.find('#')
                last: int = len(spring) - 1 - spring[::-1].find('#')
                spring = spring[last - group:first + group]
            arrangements *= len(spring) - group + 1
        return arrangements
    
    if len(springs) == 1 and len(springs[0]) == sum(groups) + len(groups) - 1:
        return 1
    
    print(springs, groups)

    if len(springs) < len(groups):
        pass


    return 0"""


"""def match_chunk(line: str, groups: Sequence[int]) -> (bool, str, list):
    chunk: int = groups[0]
    masked_chunk = re.match(r'\?[?#]*', line)
    if masked_chunk is not None and len(masked_chunk.group(0)) == chunk and '#' in masked_chunk.group(0):
        line = line.replace('?', '#', 1)

    if line.startswith('#') or '#' * chunk in line[:2 * chunk]:
        line = line.lstrip('?.')
        if len(line) < chunk or '.' in line[:chunk] or (len(line) > chunk and line[chunk] == '#'):
            return True, '#', []
        return True, line[chunk + 1:].lstrip('.'), groups[1:]
    
    return False, line, groups"""


"""def possible_arrangements(line: str, groups: Sequence[int]) -> int:
    line = line.strip('.')
    
    while True:
        # Bail conditions
        if not groups:
            return 0 if '#' in line else 1
        if not line:
            return 0
        
        # Some shortcuts when things get simple
        if len(groups) == 1:
            if '.' not in line:
                if '#' in line:
                    first: int = line.find('#')
                    last: int = len(line) - 1 - line[::-1].find('#')
                    line = line[last - group:first + group]
                else:
                    return len(line) - groups[0] + 1
                
        matched, line, groups = match_chunk(line, groups)
        if matched:
            continue
        
        matched, line, groups = match_chunk(line[::-1], groups[::-1])
        line, groups = line[::-1], groups[::-1]
        if matched:
            continue
        
        chunk: int = groups[-1]
        if line.endswith('#') or '#' * chunk in line[-2 * chunk:]:
            line = line.rstrip('?.')
            if len(line) < chunk or '.' in line[-chunk:] or (len(line) > chunk and line[-chunk - 1] == '#'):
                return 0
            line = line[:-chunk - 1].rstrip('.')
            groups = groups[:-1]
            continue
            
        # Add additional cases to pare tree
        break
    
    # line starts and ends with '?'
    return possible_arrangements(line[1:], groups) + possible_arrangements('#' + line[1:], groups)"""


def combos(chunk_len: int, groups: Sequence[int]) -> int:
    extra_space: int = chunk_len - (sum(groups) + len(groups) - 1)
    if extra_space < 0:
        return 0
    
    # print(chunk_len, groups, end='')
    # print(math.factorial(len(groups) + extra_space) // math.factorial(len(groups)) // math.factorial(extra_space))
    return math.factorial(len(groups) + extra_space) // math.factorial(len(groups)) // math.factorial(extra_space)


def possible_arrangements(line: str, groups: Sequence[int]) -> int:
    if not groups:
        return 0 if '#' in line else 1
    
    line = line.lstrip('.')
    if not line:
        return 0
    
    # if len([chunk for chunk in re.findall(r'[?#]+', line) if '#' in chunk]) > len(groups):
    #    return 0

    front_chunk: str = line.split('.', 1)[0]

    if '#' in front_chunk:
        if len(front_chunk) < groups[0]:
            return 0

        if len(front_chunk) == groups[0]:
            return possible_arrangements(line[groups[0] + 1:], groups[1:])

        if len(front_chunk) == groups[0] + 1 and not (front_chunk.startswith('#') and front_chunk.endswith('#')):
            return possible_arrangements(line[groups[0] + 2:], groups[1:])

        # len(front_chunk) > groups[0]
        if front_chunk.startswith('#'):
            if front_chunk[groups[0]] == '#':
                return 0
            return possible_arrangements(line[groups[0] + 1:], groups[1:])

        if front_chunk[groups[0]] == '#':
            return possible_arrangements(line[1:], groups)

        # line starts with '?'
        m: int = len(front_chunk) // 2 + 1
        while front_chunk[m] != '?':
            m -= 1
        return possible_arrangements(line[:m] + '.' + line[m + 1:], groups) + possible_arrangements(line[:m] + '#' + line[m + 1:], groups)

    else:
        if len(front_chunk) < groups[0]:
            return possible_arrangements(line[len(front_chunk):], groups)

        arrangements: int = possible_arrangements(line[len(front_chunk):], groups)
        for i, group in enumerate(groups):
            if sum(groups[:i + 1]) + i > len(front_chunk):
                break
            arrangements += combos(len(front_chunk), groups[:i + 1]) * possible_arrangements(line[len(front_chunk):], groups[i + 1:])
        return arrangements


def unfold(springs: str, groups: Sequence[int]) -> (list, list):
    print(f'unfolding {springs} {groups}')
    return '?'.join([springs] * 5), list(groups) * 5


def part1(data):
    """Solve part 1"""
    return sum(possible_arrangements(springs, groups) for springs, groups in data)


def part2(data):
    """Solve part 2"""
    return sum(possible_arrangements(*unfold(springs, groups)) for springs, groups in data)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 21
    PART2_TEST_ANSWER = 525152

    file = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER

    file = pathlib.Path(DIR + 'part2_test.txt')
    if file.exists() and PART2_TEST_ANSWER is not None:
        puzzle_input = file.read_text().strip()
        assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    file = pathlib.Path(DIR + 'test.txt')
    if file.exists():
        puzzle_input = file.read_text().strip()
        if PART1_TEST_ANSWER is not None:
            assert part1(parse(puzzle_input)) == PART1_TEST_ANSWER
        if PART2_TEST_ANSWER is not None:
            assert part2(parse(puzzle_input)) == PART2_TEST_ANSWER

    for file in ('input.txt',):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()