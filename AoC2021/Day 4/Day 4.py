import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    draw: list[int] = [int(n) for n in puzzle_input.split('\n')[0].split(',')]
    boards: list[list[list]] = []
    for line in puzzle_input.split('\n\n')[1:]:
        board: list[list] = [[int(n) for n in row.split()] for row in line.split('\n')]
        boards.append(board)
    return draw, boards


def mark_board(board: list[list], n: int) -> None:
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == n:
                board[i][j] = str(n)
                return


def is_complete(board: list[list]) -> bool:
    for row in board:
        if all(type(n) is str for n in row):
            return True
    for j in range(len(board[0])):
        if all(type(row[j]) is str for row in board):
            return True
    return False


def get_score(board: list[list], last_n: int) -> int:
    unmarked_sum: int = 0
    for row in board:
        for n in row:
            if type(n) is not str:
                unmarked_sum += n
    return unmarked_sum * last_n


def part1(data):
    """Solve part 1"""
    draw, boards = data
    for n in draw:
        for board in boards:
            mark_board(board, n)
            if is_complete(board):
                return get_score(board, n)


def part2(data):
    """Solve part 2"""
    draw, boards = data
    for n in draw:
        for board in boards.copy():
            mark_board(board, n)
            if is_complete(board) and len(boards) > 1:
                boards.remove(board)
        if len(boards) == 1 and is_complete(boards[0]):
            return get_score(boards[0], n)


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
