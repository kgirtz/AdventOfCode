import typing
import enum

import point


@enum.unique
class Direction(enum.Enum):
    FORWARD = 0
    FORWARD_RIGHT = 1
    RIGHT = 2
    BACKWARD_RIGHT = 3
    BACKWARD = 4
    BACKWARD_LEFT = 5
    LEFT = 6
    FORWARD_LEFT = 7


@enum.unique
class Heading(enum.Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

    def rotate(self, direction: Direction | str) -> typing.Self:
        if not isinstance(direction, Direction):
            direction = Direction[direction]
        direction = typing.cast(Direction, direction)
        return tuple(Heading)[(self.value + direction.value) % len(Heading)]


class State(typing.NamedTuple):
    position: point.Point
    heading: Heading


class PointWalker:
    @typing.overload
    def __init__(self, initial_position: point.PointTuple, initial_heading: Heading | str) -> None:
        ...

    @typing.overload
    def __init__(self, walker: typing.Self) -> None:
        ...

    def __init__(self, *args) -> None:
        # position/heading are used for shallow copy, comparison, etc
        if len(args) == 1:
            walker: PointWalker = args[0]
            self.position: point.Point = walker.position
            self.heading: Heading = walker.heading
        else:
            initial_position, initial_heading = args
            self.position = point.Point(*initial_position)
            self.heading = initial_heading if isinstance(initial_heading, Heading) else Heading[initial_heading]

        # History data is turned off by default, user can turn it on, but it isn't copied except in deepcopy()
        self.initial_state: State = self.state()
        self.track_history: bool = False
        self.history: list[State] = []
        self.visited: set[State] = set()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.position}, {self.heading})'

    def __str__(self) -> str:
        return f'({self.position.x}, {self.position.y}, {self.heading})'

    def __eq__(self, other: typing.Self) -> bool:
        return self.state() == other.state()

    def __len__(self) -> int:
        return len(self.visited_points())

    def __copy__(self) -> typing.Self:
        return self.copy()

    def __deepcopy__(self, _) -> typing.Self:
        # In addition to position/heading copy history data
        new_walker: PointWalker = self.copy()
        new_walker.initial_state = self.initial_state
        new_walker.track_history = self.track_history
        new_walker.history = self.history.copy()
        new_walker.visited = self.visited.copy()
        return new_walker

    def copy(self) -> typing.Self:
        # Only copy position/heading, history data is ignored
        return PointWalker(self.position, self.heading)

    def state(self) -> State:
        return State(self.position, self.heading)

    def next(self) -> point.Point:
        return self.peek()

    def peek(self, direction: Direction | str = Direction.FORWARD, *, distance: int = 1) -> point.Point:
        peek_heading: Heading = self.heading.rotate(direction)
        match peek_heading:
            case Heading.NORTH:
                return self.position.up(distance)
            case Heading.NORTHEAST:
                return self.position.up_right(distance)
            case Heading.EAST:
                return self.position.right(distance)
            case Heading.SOUTHEAST:
                return self.position.down_right(distance)
            case Heading.SOUTH:
                return self.position.down(distance)
            case Heading.SOUTHWEST:
                return self.position.down_left(distance)
            case Heading.WEST:
                return self.position.left(distance)
            case Heading.NORTHWEST:
                return self.position.up_left(distance)

    def step(self) -> None:
        self.move()

    def move(self, distance: int = 1, direction: Direction | str = Direction.FORWARD) -> None:
        self.record()
        self.position = self.peek(direction, distance=distance)

    def turn(self, direction: Direction | str) -> None:
        self.record()
        self.heading = self.heading.rotate(direction)

    def record(self) -> None:
        if self.track_history:
            self.history.append(self.state())
            self.visited.add(self.state())

    def visited_points(self) -> set[point.Point]:
        return {pt for pt, _ in self.history} | {self.position}

    def initial_position(self) -> point.Point:
        return self.initial_state.position

    def initial_heading(self) -> Heading:
        return self.initial_state.heading

    def has_looped(self) -> bool:
        return self.state() in self.visited

    def returned_to_start(self) -> bool:
        return self.state() == self.initial_state
