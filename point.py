import typing
import math

PointTuple: typing.TypeAlias = tuple[int, int]


class Point(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def __str__(self) -> str:
        return str(tuple(self))

    def left(self) -> typing.Self:
        return Point(self.x - 1, self.y)

    def right(self) -> typing.Self:
        return Point(self.x + 1, self.y)

    def above(self) -> typing.Self:
        return Point(self.x, self.y - 1)

    def below(self) -> typing.Self:
        return Point(self.x, self.y + 1)

    def up_left(self) -> typing.Self:
        return self.above().left()

    def down_left(self) -> typing.Self:
        return self.below().left()

    def up_right(self) -> typing.Self:
        return self.above().right()

    def down_right(self) -> typing.Self:
        return self.below().right()

    def is_left_of(self, pt: PointTuple) -> bool:
        return self.right() == pt

    def is_right_of(self, pt: PointTuple) -> bool:
        return self.left() == pt

    def is_above(self, pt: PointTuple) -> bool:
        return self.below() == pt

    def is_below(self, pt: PointTuple) -> bool:
        return self.above() == pt

    def is_adjacent(self, pt: PointTuple, *, diagonal: bool = False) -> bool:
        return pt in self.neighbors(diagonal=diagonal)

    def neighbors(self, *, diagonal: bool = False) -> set[typing.Self]:
        if diagonal:
            return {self.above(),
                    self.below(),
                    self.left(),
                    self.right(),
                    self.up_right(),
                    self.up_left(),
                    self.down_right(),
                    self.down_left()}

        return {self.above(),
                self.below(),
                self.left(),
                self.right()}

    def distance(self, start: PointTuple = (0, 0)) -> float:
        start = Point(*start)
        return math.hypot(self.x - start.x, self.y - start.y)

    def manhattan_distance(self, start: PointTuple = (0, 0)) -> int:
        start = Point(*start)
        return abs(self.x - start.x) + abs(self.y - start.y)


ORIGIN: Point = Point(0, 0)
