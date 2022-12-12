from pathlib import Path
from typing import Iterator


class Grid:
    lines: list[list[str]]
    pos: tuple[int, int]
    target: tuple[int, int]
    best: int = 10000

    def __init__(self, file_name: str):
        self.lines = [
            list(iter(line)) for line in Path(file_name).read_text().splitlines()
        ]
        for y, line in enumerate(self.lines):
            for x, s in enumerate(line):
                if s == "S":
                    self.lines[y][x] = "a"
                    self.pos = (y, x)
                elif s == "E":
                    self.lines[y][x] = "z"
                    self.target = (y, x)

    def __str__(self):
        return f"""player: {self.pos}
target: {self.target}
""" + "\n".join(
            ["".join(line) for line in self.lines]
        )

    def elevation(self, src: tuple[int, int], dst: tuple[int, int]):
        if (
            dst[0] < 0
            or dst[0] >= len(self.lines)
            or dst[1] >= len(self.lines[dst[0]])
            or dst[1] < 0
        ):
            return 1000
        diff = ord(self.lines[dst[0]][dst[1]]) - ord(self.lines[src[0]][src[1]])
        return diff

    def posible_movements(self, pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        for ydiff in (-1, 1):
            if self.elevation(pos, (pos[0] + ydiff, pos[1])) <= 1:
                yield (pos[0] + ydiff, pos[1])
        for xdiff in (-1, 1):
            if self.elevation(pos, (pos[0], pos[1] + xdiff)) <= 1:
                yield (pos[0], pos[1] + xdiff)

    def traverse(self, start_pos=None):
        if start_pos:
            self.pos = start_pos
        distances = {self.pos: (0, None)}
        while self.target not in distances:
            prev_keys = list(distances.keys())
            progress = False
            for q in prev_keys:
                cost, prev = distances[q]
                for new_pos in self.posible_movements(q):
                    if new_pos not in distances:
                        distances[new_pos] = cost + 1, q
                        progress = True
            if not progress:
                return

        return distances

    def starting_positions(self):
        return [
            (y, x)
            for y, row in enumerate(self.lines)
            for x, c in enumerate(row)
            if c == "a"
        ]


grid = Grid("input12.txt")
m = grid.traverse()
print(f"Part1: {m[grid.target][0]}")

min_2 = min(
    [
        z[grid.target][0]
        for start_pos in grid.starting_positions()
        if (z := grid.traverse(start_pos))
    ]
)

print(f"Part2: {min_2}")
