import typing
import collections

import xypair


class Space:
    def __init__(self, space_str: str | typing.Sequence[str], item_types: typing.Iterable[str] = tuple(), *, default: str = '.') -> None:
        if isinstance(space_str, str):
            space_str = space_str.split('\n')
        else:
            space_str = list(space_str)

        self.height: int = len(space_str)
        self.width: int = len(space_str[0])
        self.tiles: list[str] = space_str
        self.items: dict[str, set[xypair.XYpair]] = collections.defaultdict(set)
        self.integer_values: bool = False
        self.default: str = default

        for y, line in enumerate(space_str):
            for x, tile in enumerate(line):
                if (not item_types and tile != self.default) or tile in item_types:
                    self.items[tile].add(xypair.XYpair(x, y))
        self.items = dict(self.items)

    def __str__(self) -> str:
        return '\n'.join(self.tiles)

    @xypair.accept_tuple_method
    def __getitem__(self, pt: xypair.XYpair) -> str:
        value: str = self.tiles[pt.y][pt.x]
        return int(value) if self.integer_values else value

    @xypair.accept_tuple_method
    def in_space(self, pt: xypair.XYpair) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def on_edge(self, pt: xypair.XYtuple) -> bool:
        return self.on_top_edge(pt) or self.on_bottom_edge(pt) or self.on_left_edge(pt) or self.on_right_edge(pt)

    @staticmethod
    @xypair.accept_tuple
    def on_top_edge(pt: xypair.XYpair) -> bool:
        return pt.y == 0

    @xypair.accept_tuple_method
    def on_bottom_edge(self, pt: xypair.XYpair) -> bool:
        return pt.y == self.height - 1

    @staticmethod
    @xypair.accept_tuple
    def on_left_edge(pt: xypair.XYpair) -> bool:
        return pt.x == 0

    @xypair.accept_tuple_method
    def on_right_edge(self, pt: xypair.XYpair) -> bool:
        return pt.x == self.width - 1

    @xypair.accept_tuple_method
    def neighbors(self, pt: xypair.XYpair, *args, **kwargs) -> set[xypair.XYpair]:
        return {n for n in pt.neighbors(*args, **kwargs) if self.in_space(n)}

    def initial_position(self, item: str) -> xypair.XYpair:
        pts: tuple[xypair.XYpair, ...] = tuple(self.items[item])
        if len(pts) != 1:
            raise ValueError(f"more than one '{item}' found")
        return pts[0]
