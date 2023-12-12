import pathlib
import sys
import os


def parse(puzzle_input):
    """Parse input"""
    commands: list[str] = [c for c in puzzle_input.split('$') if c]
    return [command.strip().split('\n') for command in commands]


def build_dir_list(listing: list[list[str]]) -> list[dict[str, ...]]:
    root: dict[str, dict] = {'/': {}}

    dir_list: list[dict[str, ...]] = [root]

    cur_dir: dict[str, dict] = root
    for command in listing:
        cmd = command[0].split()[0]
        match cmd:
            case 'cd':
                arg: str = command[0].split()[1]
                if arg == '/':
                    cur_dir = root
                else:
                    cur_dir = cur_dir[arg]

            case 'ls':
                for output in command[1:]:
                    t, name = output.split()
                    if t == 'dir':
                        cur_dir[name] = {'..': cur_dir}
                        dir_list.append(cur_dir[name])
                    else:
                        cur_dir[name] = {'size': int(t)}

    return dir_list


def dir_size(d: dict[str, ...]) -> int:
    size: int = 0

    for name, contents in d.items():
        match name:
            case '..':
                continue
            case 'size':
                return contents
            case _:
                size += dir_size(contents)

    return size


def part1(data):
    """Solve part 1"""
    dir_list: list[dict[str, ...]] = build_dir_list(data)

    dir_sizes: list[int] = [dir_size(d) for d in dir_list]

    return sum([s for s in dir_sizes if s <= 100000])


def part2(data):
    """Solve part 2"""
    dir_list: list[dict[str, ...]] = build_dir_list(data)

    dir_sizes: list[int] = [dir_size(d) for d in dir_list]

    excess_mem: int = dir_sizes[0] - 40000000

    return min([d for d in dir_sizes if d >= excess_mem])


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
