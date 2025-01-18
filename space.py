import collections

import xypair


class Space:
    def __init__(self,
                 space_str: str | collections.abc.Sequence[str],
                 item_types: collections.abc.Container[str] = tuple(),
                 *,
                 default: str = '.') -> None:

        if isinstance(space_str, str):
            space_str = space_str.split('\n')
        else:
            space_str = list(space_str)

        self.height: int = len(space_str)
        self.width: int = max(len(s) for s in space_str)
        self.items: dict[str, set[xypair.XYpair]] = collections.defaultdict(set)
        self.integer_values: bool = False
        self.default: str = default

        for y, line in enumerate(space_str):
            for x, tile in enumerate(line):
                if (not item_types and tile != self.default) or tile in item_types:
                    self.items[tile].add(xypair.XYpair(x, y))
        self.items = dict(self.items)

    def __str__(self) -> str:
        lines: list[str] = []
        for y in range(self.height):
            line: str = ''
            for x in range(self.width):
                value: str = self.default
                for item, pts in self.items.items():
                    if (x, y) in pts:
                        value = item
                        break
                line += value
            lines.append(line)
        return '\n'.join(lines)

    @xypair.accept_tuple_method
    def __getitem__(self, pt: xypair.XYpair) -> str:
        value: str = self.default
        for item, pts in self.items.items():
            if pt in pts:
                value = item
                break

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

    @xypair.accept_tuple_method
    def surrounding(self, pt: xypair.XYpair, radius: int) -> set[xypair.XYpair]:
        pts: set[xypair.XYpair] = set()
        edge: set[xypair.XYpair] = {pt}
        for _ in range(radius):
            new_edge: set[xypair.XYpair] = set()
            while edge:
                pt: xypair.XYpair = edge.pop()
                new_edge.update(n for n in pt.neighbors() - pts if self.in_space(n))
                pts.add(pt)
            edge = new_edge
            pts.update(edge)

        pts.discard(pt)
        return pts

    def initial_position(self, item: str) -> xypair.XYpair:
        pts: list[xypair.XYpair] = list(self.items[item])
        if len(pts) > 1:
            raise ValueError(f"more than one {item} found")
        return pts.pop()
