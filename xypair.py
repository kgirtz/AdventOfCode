import typing
import math
import functools
import collections.abc

XYtuple: typing.TypeAlias = tuple[int, ...]


def accept_tuple(func: collections.abc.Callable) -> collections.abc.Callable:
    @functools.wraps(func)
    def wrapper(pair_or_tuple: XYtuple, *args, **kwargs):
        return func(XYpair(*pair_or_tuple), *args, **kwargs)
    return wrapper


def accept_tuple_method(func: collections.abc.Callable) -> collections.abc.Callable:
    @functools.wraps(func)
    def wrapper(self, pair_or_tuple: XYtuple, *args, **kwargs):
        return func(self, XYpair(*pair_or_tuple), *args, **kwargs)
    return wrapper


@typing.final
class XYpair(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    def __bool__(self) -> bool:
        return self != ORIGIN

    def left(self, distance: int = 1) -> typing.Self:
        return XYpair(self.x - distance, self.y)

    def right(self, distance: int = 1) -> typing.Self:
        return XYpair(self.x + distance, self.y)

    def up(self, distance: int = 1) -> typing.Self:
        return XYpair(self.x, self.y - distance)

    def down(self, distance: int = 1) -> typing.Self:
        return XYpair(self.x, self.y + distance)

    def up_left(self, distance: int = 1) -> typing.Self:
        return self.up(distance).left(distance)

    def down_left(self, distance: int = 1) -> typing.Self:
        return self.down(distance).left(distance)

    def up_right(self, distance: int = 1) -> typing.Self:
        return self.up(distance).right(distance)

    def down_right(self, distance: int = 1) -> typing.Self:
        return self.down(distance).right(distance)

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

    def adjacent(self, pt: XYtuple, *, include_corners: bool = False) -> bool:
        return pt in self.neighbors(include_corners=include_corners)

    def collinear(self, pts: typing.Iterable[XYtuple]) -> bool:
        pts = list(pts)
        basis: XYpair = self - XYpair(*pts[0])
        for pt in pts:
            diff: XYpair = self - pt
            if diff.x / basis.x != diff.y / basis.y:
                return False
        return True

    def neighbors(self, *, include_corners: bool = False, corners_only: bool = False) -> set[typing.Self]:
        diagonal: set[XYpair] = {self.up_right(), self.up_left(), self.down_right(), self.down_left()}
        if corners_only:
            return diagonal

        orthogonal: set[XYpair] = {self.up(), self.down(), self.left(), self.right()}
        if include_corners:
            return orthogonal | diagonal

        return orthogonal

    def surrounding(self, radius: int) -> set[typing.Self]:
        pts: set[XYpair] = set()
        edge: set[XYpair] = {self}
        for _ in range(radius):
            new_edge: set[XYpair] = set()
            while edge:
                pt: XYpair = edge.pop()
                new_edge.update(pt.neighbors() - pts)
                pts.add(pt)
            edge = new_edge
            pts.update(edge)

        pts.discard(self)
        return pts

    @accept_tuple_method
    def distance(self, start: typing.Self) -> float:
        return math.hypot(self.x - start.x, self.y - start.y)

    @accept_tuple_method
    def manhattan_distance(self, start: typing.Self) -> int:
        return abs(self.x - start.x) + abs(self.y - start.y)

    def __add__(self, other: XYtuple) -> typing.Self:
        if isinstance(other, tuple):
            other = XYpair(*other)
            return XYpair(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __radd__(self, other: typing.Any) -> typing.Self:
        return self + other

    def __sub__(self, other: XYtuple) -> typing.Self:
        if isinstance(other, tuple):
            other = XYpair(*other)
            return XYpair(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __rsub__(self, other: XYtuple) -> XYtuple:
        if isinstance(other, tuple):
            other = XYpair(*other)
            return other.x - self.x, other.y - self.y
        return NotImplemented

    def __mul__(self, other: int) -> typing.Self:
        if isinstance(other, int):
            return XYpair(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: typing.Any) -> typing.Self:
        return self * other

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return XYpair(-self.x, -self.y)

    def __abs__(self) -> float:
        return self.distance(ORIGIN)


ORIGIN: XYpair = XYpair(0, 0)
