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

    def __bool__(self) -> bool:
        return self != ORIGIN

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

    @accept_tuple_method
    def is_left_of(self, pt: typing.Self) -> bool:
        return self.x < pt.x

    @accept_tuple_method
    def is_right_of(self, pt: typing.Self) -> bool:
        return self.x > pt.x

    @accept_tuple_method
    def is_above(self, pt: typing.Self) -> bool:
        return self.y < pt.y

    @accept_tuple_method
    def is_below(self, pt: typing.Self) -> bool:
        return self.y > pt.y

    @accept_tuple_method
    def same_column(self, pt: typing.Self) -> bool:
        return self.x == pt.x

    @accept_tuple_method
    def same_row(self, pt: typing.Self) -> bool:
        return self.y == pt.y

    def adjacent(self, pt: PointTuple, *, include_corners: bool = False) -> bool:
        return pt in self.neighbors(include_corners=include_corners)

    def neighbors(self, *, include_corners: bool = False, corners_only: bool = False) -> set[typing.Self]:
        diagonal: set[Point] = {self.up_right(), self.up_left(), self.down_right(), self.down_left()}
        if corners_only:
            return diagonal

        orthogonal: set[Point] = {self.up(),  self.down(), self.left(), self.right()}
        if include_corners:
            return orthogonal | diagonal

        return orthogonal

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

    def __add__(self, other: PointTuple) -> typing.Self:
        if isinstance(other, tuple):
            other = Point(*other)
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __radd__(self, other: typing.Any) -> typing.Self:
        return self + other

    def __sub__(self, other: PointTuple) -> typing.Self:
        if isinstance(other, tuple):
            other = Point(*other)
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __rsub__(self, other: PointTuple) -> PointTuple:
        if isinstance(other, tuple):
            other = Point(*other)
            return other.x - self.x, other.y - self.y
        return NotImplemented

    def __mul__(self, other: int) -> typing.Self:
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: typing.Any) -> typing.Self:
        return self * other

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return Point(-self.x, -self.y)

    def __abs__(self) -> float:
        return self.distance(ORIGIN)


ORIGIN: Point = Point(0, 0)
