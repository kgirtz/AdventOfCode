import pathlib
import sys
import os

from space import Space
from point import Point


def parse(puzzle_input: str):
    """Parse input"""
    return Space(puzzle_input.split('\n'), 'XMAS')


def count_words(word: str, start: Point, s: Space) -> int:
    assert len(word) > 1 and word[0] == s[start]

    directions: tuple[str, ...] = ('right',
                                   'down_right',
                                   'below',
                                   'down_left',
                                   'left',
                                   'up_left',
                                   'above',
                                   'up_right')

    total: int = 0
    for d in directions:
        pt: Point = start
        word_idx: int = 1
        next_pt: Point = getattr(pt, d)()
        while s.in_space(next_pt) and s[next_pt] == word[word_idx]:
            if word_idx == len(word) - 1:
                total += 1
                break
            pt = next_pt
            next_pt = getattr(pt, d)()
            word_idx += 1
    return total


def is_x(word: str, center: Point, s: Space) -> bool:
    assert word[1] == s[center] and len(word) == 3
    if s.on_edge(center):
        return False

    return s[center.up_left()] != s[center.down_right()] and \
           s[center.down_left()] != s[center.up_right()] and \
           all(s[c] in (word[0], word[-1]) for c in center.neighbors(corners_only=True))


def part1(data):
    """Solve part 1"""
    word: str = 'XMAS'
    return sum(count_words(word, pt, data) for pt in data.items[word[0]])


def part2(data):
    """Solve part 2"""
    word: str = 'MAS'
    return sum(is_x(word, pt, data) for pt in data.items[word[1]])


def solve(puzzle_input: str):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == '__main__':
    DIR: str = f'{os.path.dirname(sys.argv[0])}/'

    PART1_TEST_ANSWER = 18
    PART2_TEST_ANSWER = 9

    file: pathlib.Path = pathlib.Path(DIR + 'part1_test.txt')
    if file.exists() and PART1_TEST_ANSWER is not None:
        puzzle_input: str = file.read_text().strip()
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

    for infile in ('input.txt',):
        print(f'{infile}:')
        puzzle_input = pathlib.Path(DIR + infile).read_text().strip()
        solutions = solve(puzzle_input)
        print('\n'.join(str(solution) for solution in solutions))
        print()
