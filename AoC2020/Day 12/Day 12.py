import pathlib
import sys
import os

compass: dict[int, str] = {0: 'E', 90: 'N', 180: 'W', 270: 'S'}


def parse(puzzle_input):
    """Parse input"""
    return [line for line in puzzle_input.split('\n')]


class Ship:
    def __init__(self) -> None:
        self.direction: int = 0
        self.longitude: int = 0
        self.latitude: int = 0
        self.waypoint_lat: int = 1
        self.waypoint_long: int = 10

    def shift(self, direction: str, amount: int) -> None:
        if direction == 'N':
            self.latitude += amount
        elif direction == 'S':
            self.latitude -= amount
        elif direction == 'E':
            self.longitude += amount
        elif direction == 'W':
            self.longitude -= amount

    def rotate(self, direction: str, amount: int) -> None:
        if direction == 'L':
            self.direction = (self.direction + amount) % 360
        elif direction == 'R':
            self.direction = (self.direction - amount + 360) % 360

    def forward(self, distance: int) -> None:
        self.shift(compass[self.direction], distance)

    def shift_waypoint(self, direction: str, amount: int) -> None:
        if direction == 'N':
            self.waypoint_lat += amount
        elif direction == 'S':
            self.waypoint_lat -= amount
        elif direction == 'E':
            self.waypoint_long += amount
        elif direction == 'W':
            self.waypoint_long -= amount

    def rotate_waypoint(self, direction: str, amount: int) -> None:
        if direction == 'R':
            amount = 360 - amount

        for _ in range(amount // 90):
            self.waypoint_long, self.waypoint_lat = -self.waypoint_lat, self.waypoint_long

    def move_to_waypoint(self, moves: int) -> None:
        for _ in range(moves):
            self.latitude += self.waypoint_lat
            self.longitude += self.waypoint_long

    def perform_action(self, action: str) -> None:
        action_type: str = action[0]
        action_value: int = int(action[1:])

        if action_type in 'NSEW':
            self.shift(action_type, action_value)
        elif action_type in 'LR':
            self.rotate(action_type, action_value)
        elif action_type == 'F':
            self.forward(action_value)

    def perform_action_waypoint(self, action: str) -> None:
        action_type: str = action[0]
        action_value: int = int(action[1:])

        if action_type in 'NSEW':
            self.shift_waypoint(action_type, action_value)
        elif action_type in 'LR':
            self.rotate_waypoint(action_type, action_value)
        elif action_type == 'F':
            self.move_to_waypoint(action_value)

    def distance_from_launch(self) -> int:
        return abs(self.latitude) + abs(self.longitude)


def part1(data):
    """Solve part 1"""
    ship: Ship = Ship()
    for action in data:
        ship.perform_action(action)
    return ship.distance_from_launch()


def part2(data):
    """Solve part 2"""
    ship: Ship = Ship()
    for action in data:
        ship.perform_action_waypoint(action)
    return ship.distance_from_launch()


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
