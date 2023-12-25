import typing
import math


class Point(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def left(self) -> 'Point':
        return Point(self.x - 1, self.y)

    def right(self) -> 'Point':
        return Point(self.x + 1, self.y)

    def above(self) -> 'Point':
        return Point(self.x, self.y - 1)

    def below(self) -> 'Point':
        return Point(self.x, self.y + 1)

    def up_left(self) -> 'Point':
        return Point(self.x - 1, self.y - 1)

    def down_left(self) -> 'Point':
        return Point(self.x - 1, self.y + 1)

    def up_right(self) -> 'Point':
        return Point(self.x + 1, self.y - 1)

    def down_right(self) -> 'Point':
        return Point(self.x + 1, self.y + 1)

    def is_left_of(self, pt: 'Point') -> bool:
        return self.x + 1 == pt.x and self.y == pt.y

    def is_right_of(self, pt: 'Point') -> bool:
        return self.x - 1 == pt.x and self.y == pt.y

    def is_above(self, pt: 'Point') -> bool:
        return self.x == pt.x and self.y + 1 == pt.y

    def is_below(self, pt: 'Point') -> bool:
        return self.x == pt.x and self.y - 1 == pt.y

    def is_adjacent_to(self, pt: 'Point') -> bool:
        return self.is_above(pt) or self.is_below(pt) or self.is_left_of(pt) or self.is_right_of(pt)

    def neighbors(self, *, diagonals: bool = False) -> set['Point']:
        pts: set[Point] = {
            self.above(),
            self.below(),
            self.left(),
            self.right()
                           }

        if diagonals:
            pts |= {
                self.up_right(),
                self.up_left(),
                self.down_right(),
                self.down_left()
                    }

        return pts

    def distance(self, start: 'Point' = None) -> float:
        if start is None:
            start = ORIGIN

        return math.sqrt((self.x - start.x) ** 2 + (self.y - start.y) ** 2)

    def manhattan_distance(self, start: 'Point' = None) -> int:
        if start is None:
            start = ORIGIN

        return abs(self.x - start.x) + abs(self.y - start.y)


ORIGIN: Point = Point(0, 0)
