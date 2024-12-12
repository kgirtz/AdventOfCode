import typing
import math
import functools

PointTuple: typing.TypeAlias = tuple[int, ...]


def accept_tuple(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrapper(point_or_tuple: PointTuple, *args, **kwargs):
        return func(Point(*point_or_tuple), *args, **kwargs)
    return wrapper


def accept_tuple_method(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrapper(self, point_or_tuple: PointTuple, *args, **kwargs):
        return func(self, Point(*point_or_tuple), *args, **kwargs)
    return wrapper


class Point(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    def left(self) -> typing.Self:
        return Point(self.x - 1, self.y)

    def right(self) -> typing.Self:
        return Point(self.x + 1, self.y)

    def up(self) -> typing.Self:
        return Point(self.x, self.y - 1)

    def down(self) -> typing.Self:
        return Point(self.x, self.y + 1)

    def up_left(self) -> typing.Self:
        return self.up().left()

    def down_left(self) -> typing.Self:
        return self.down().left()

    def up_right(self) -> typing.Self:
        return self.up().right()

    def down_right(self) -> typing.Self:
        return self.down().right()

    def is_left_of(self, pt: PointTuple) -> bool:
        return self.right() == pt

    def is_right_of(self, pt: PointTuple) -> bool:
        return self.left() == pt

    def is_above(self, pt: PointTuple) -> bool:
        return self.down() == pt

    def is_below(self, pt: PointTuple) -> bool:
        return self.up() == pt

    def adjacent(self, pt: PointTuple, *, include_corners: bool = False) -> bool:
        return pt in self.neighbors(include_corners=include_corners)

    def neighbors(self, *, include_corners: bool = False, corners_only: bool = False) -> set[typing.Self]:
        if corners_only:
            return {self.up_right(),
                    self.up_left(),
                    self.down_right(),
                    self.down_left()}

        if include_corners:
            return {self.up(),
                    self.down(),
                    self.left(),
                    self.right(),
                    self.up_right(),
                    self.up_left(),
                    self.down_right(),
                    self.down_left()}

        return {self.up(),
                self.down(),
                self.left(),
                self.right()}

    @accept_tuple_method
    def distance(self, start: typing.Self) -> float:
        return math.hypot(self.x - start.x, self.y - start.y)

    @accept_tuple_method
    def manhattan_distance(self, start: typing.Self) -> int:
        return abs(self.x - start.x) + abs(self.y - start.y)

    @accept_tuple_method
    def run(self, other: typing.Self) -> int:
        return other.x - self.x

    @accept_tuple_method
    def rise(self, other: typing.Self) -> int:
        return other.y - self.y


ORIGIN: Point = Point(0, 0)
