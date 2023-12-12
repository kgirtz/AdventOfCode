import pathlib
import sys
import os
from collections import namedtuple, deque
from typing import Optional
from math import inf

Location = namedtuple('Location', 'room pos')
room_pos: dict[str, int] = {'A': 2, 'B': 4, 'C': 6, 'D': 8}


def parse(puzzle_input):
    """Parse input"""
    return State(puzzle_input)


def energy_rate(a: str) -> int:
    if a == 'A':
        return 1
    if a == 'B':
        return 10
    if a == 'C':
        return 100
    if a == 'D':
        return 1000


def in_hallway(pos: Location) -> bool:
    return pos.room == 'H'


class State:
    def __init__(self, configuration: str = '', energy: int = 0) -> None:
        self.energy: int = energy
        self.room_size: int = 0
        self.rooms: dict[str, list[str]] = {}
        self.hallway: list[str] = []
        if configuration:
            diagram: list[str] = [line.strip().strip('#') for line in configuration.split('\n')]
            self.room_size = len(diagram) - 3
            self.hallway: list[str] = list(diagram[1])
            room_contents: list[list[str]] = [row.split('#') for row in diagram[2:-1]]
            for i, amphipod in enumerate('ABCD'):
                self.rooms[amphipod] = [row[i] for row in room_contents]

    def __str__(self) -> str:
        configuration: str = "#############\n"
        configuration += f"#{''.join(self.hallway)}#\n"

        print_rooms: dict[str, list[str]] = {room: contents.copy() for room, contents in self.rooms.items()}
        for room in print_rooms.values():
            while len(room) < self.room_size:
                room.insert(0, '.')

        configuration += f"###{'#'.join(print_rooms[a][0] for a in 'ABCD')}###\n"
        for i in range(1, self.room_size):
            configuration += f"  #{'#'.join(print_rooms[a][i] for a in 'ABCD')}#\n"
        configuration += "  #########\n"

        return configuration

    def key(self) -> str:
        key_str: str = ''.join(self.hallway)
        for room in self.rooms.values():
            key_str += ''.join(room)
        return key_str

    def copy(self) -> 'State':
        new_state: State = State(energy=self.energy)
        new_state.room_size = self.room_size
        new_state.hallway = self.hallway.copy()
        new_state.rooms = {room: contents.copy() for room, contents in self.rooms.items()}
        return new_state

    def hallway_empty(self) -> bool:
        for space in self.hallway:
            if space != '.':
                return False
        return True

    def has_visitors(self, a: str) -> bool:
        for space in self.rooms[a]:
            if space not in (a, '.'):
                return True
        return False

    def space_available(self, a: str) -> Optional[Location]:
        room: list[str] = self.rooms[a]
        if room[0] == a or self.has_visitors(a):
            return None

        for i, space in enumerate(room):
            if space == a:
                return Location(a, i - 1)
        return Location(a, len(room) - 1)

    def path_clear(self, src: Location, dst: Location) -> bool:
        hall_spaces: list[int] = []

        if not in_hallway(src):
            for space in self.rooms[src.room][:src.pos]:
                if space != '.':
                    return False
            hall_spaces.append(room_pos[src.room])

        if not in_hallway(dst):
            for space in self.rooms[dst.room][:dst.pos + 1]:
                if space != '.':
                    return False
            hall_spaces.append(room_pos[dst.room])

        if len(hall_spaces) < 2:
            if in_hallway(src):
                if src.pos < hall_spaces[0]:
                    hall_spaces.append(src.pos + 1)
                else:
                    hall_spaces.append(src.pos - 1)
            else:
                hall_spaces.append(dst.pos)

        left: int = min(hall_spaces)
        right: int = max(hall_spaces)
        for space in self.hallway[left:right + 1]:
            if space != '.':
                return False

        return True

    def move(self, src: Location, dst: Location) -> None:
        if src.room == 'H':
            energy_consumed: int = energy_rate(self.hallway[src.pos])
        else:
            energy_consumed = energy_rate(self.rooms[src.room][src.pos])

        spaces: int = 0
        if src.room != 'H' and dst.room != 'H':
            spaces += src.pos + dst.pos + 1
            spaces += abs(room_pos[src.room] - room_pos[dst.room]) + 1
            self.rooms[src.room][src.pos], self.rooms[dst.room][dst.pos] \
                = self.rooms[dst.room][dst.pos], self.rooms[src.room][src.pos]
        elif src.room == 'H':
            spaces += dst.pos + 1
            spaces += abs(src.pos - room_pos[dst.room])
            self.hallway[src.pos], self.rooms[dst.room][dst.pos] = self.rooms[dst.room][dst.pos], self.hallway[src.pos]
        elif dst.room == 'H':
            spaces += src.pos
            spaces += abs(room_pos[src.room] - dst.pos) + 1
            self.rooms[src.room][src.pos], self.hallway[dst.pos] = self.hallway[dst.pos], self.rooms[src.room][src.pos]

        self.energy += spaces * energy_consumed

    def move_home(self) -> None:
        moved: bool = True
        while moved:
            moved = False
            for i, hall_space in enumerate(self.hallway):
                if hall_space != '.':
                    home: Optional[Location] = self.space_available(hall_space)
                    if home:
                        pos: Location = Location('H', i)
                        if self.path_clear(pos, home):
                            self.move(pos, home)
                            moved = True

            for room, contents in self.rooms.items():
                if not self.has_visitors(room):
                    continue

                top: int = 0
                while contents[top] == '.':
                    top += 1

                dst: str = contents[top]
                if dst != room:
                    home: Optional[Location] = self.space_available(dst)
                    if home:
                        pos: Location = Location(room, top)
                        if self.path_clear(pos, home):
                            self.move(pos, home)
                            moved = True

    def possible_moves(self) -> list['State']:
        moves: list[State] = []
        for room, contents in self.rooms.items():
            if not self.has_visitors(room):
                continue

            top: int = 0
            while contents[top] == '.':
                top += 1
            start: Location = Location(room, top)

            for i, hall_space in enumerate(self.hallway):
                if hall_space == '.' and i not in room_pos.values():
                    target: Location = Location('H', i)
                    if self.path_clear(start, target):
                        new_state: State = self.copy()
                        new_state.move(start, target)
                        if new_state.valid():
                            moves.append(new_state)
        return moves

    def valid(self) -> bool:
        for i, a in enumerate(self.hallway):
            if a == '.':
                continue

            dst: int = room_pos[a]
            if i < dst:
                for b in self.hallway[i + 1:dst + 1]:
                    if b != '.' and room_pos[b] < i:
                        return False
            elif dst < i:
                for b in self.hallway[dst:i]:
                    if b != '.' and room_pos[b] > i:
                        return False
        return True

    def complete(self) -> bool:
        if not self.hallway_empty():
            return False
        for room in self.rooms:
            if self.has_visitors(room):
                return False
        return True


def brute_force(initial: State) -> int:
    min_energy: [int, float] = inf
    states: deque[State] = deque([initial])
    seen: dict[str, int] = {}
    while states:
        for state in states.popleft().possible_moves():
            if state.energy >= min_energy:
                continue

            state.move_home()
            if state.energy < min_energy:
                if state.complete():
                    min_energy = state.energy
                else:
                    key: str = state.key()
                    if key not in seen or state.energy < seen[key]:
                        states.append(state)
                        seen[key] = state.energy
    return min_energy


def part1(data):
    """Solve part 1"""
    if data.room_size == 4:
        data.room_size = 2
        for room in data.rooms.values():
            del room[1:3]
    return brute_force(data)


def part2(data):
    """Solve part 2"""
    return brute_force(data)


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
        puzzle_input = pathlib.Path('./' + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
