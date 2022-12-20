from pathlib import Path
from dataclasses import dataclass
from itertools import cycle

movements = Path("input17.txt").read_text().strip()


shapes = [
    ["@@@@"],
    [".@.", "@@@", ".@."],
    ["..@", "..@", "@@@"],
    ["@", "@", "@", "@"],
    ["@@", "@@"],
]
start_positions = [()]


def shape_len(shape: list[str]):
    return max([s.rindex("@") for s in shape]) + 1


@dataclass
class Sprite:
    x: int
    y: int
    shape: list[str]


class Game:
    board = []
    current_sprite: Sprite | None

    def __init__(self):
        self.board = []
        self.current_sprite = None

    def freepos_y(self):
        for i, row in enumerate(self.board):
            if "#" in row or "-" in row:
                return i - 1
        return len(self.board) - 1

    def place_item(self, shape: list[str]):
        if not self.board or self.freepos_y() - len(shape) < 10:  # Ensure enough space
            self.board = ["       "] * 7 + self.board  # extend board
        y = self.freepos_y() - 2 - len(shape)

        x = 2
        self.current_sprite = Sprite(x, y, shape)

    def push(self, s: str):
        match s:
            case "<":
                if self.current_sprite.x > 0:
                    self.current_sprite.x -= 1
                    if self.colides():
                        self.current_sprite.x += 1  # revert
            case ">":
                if self.current_sprite.x + shape_len(self.current_sprite.shape) < 7:
                    self.current_sprite.x += 1
                    if self.colides():
                        self.current_sprite.x -= 1  # revert
            case _:
                raise ValueError(f"Invalid movement {s}")

    def colides(self) -> bool:
        s = self.current_sprite
        for y in range(0, len(s.shape)):
            if y + s.y >= len(self.board):
                return True
            for x in range(len(s.shape[y])):
                if s.shape[y][x] == "@" and self.board[y + s.y][x + s.x] == "#":
                    return True
        return False

    def freeze(self):
        s = self.current_sprite
        for y in range(0, len(s.shape)):
            self.board[y + s.y] = (
                self.board[y + s.y][: s.x]
                + "".join(
                    [
                        "#" if s == "@" else b
                        for b, s in zip(self.board[y + s.y][s.x :], s.shape[y])
                    ]
                )
                + self.board[y + s.y][s.x + len(s.shape[y]) :]
            )
        self.current_sprite = None

    def fall(self) -> bool:
        self.current_sprite.y += 1
        if self.colides():
            self.current_sprite.y -= 1  # revert
            self.freeze()
            return False
        return True

    def height(self) -> int:
        return len(self.board) - self.freepos_y() - 1

    def __str__(self):
        merged_rows = []
        for y, row in enumerate(self.board):
            s = self.current_sprite
            if s and y in range(s.y, s.y + len(s.shape)):
                current_line = (
                    self.board[y][: s.x]
                    + "".join(
                        [
                            b if s == "." else s
                            for (b, s) in zip(self.board[y][s.x :], s.shape[y - s.y])
                        ]
                    )
                    + self.board[y][s.x + len(s.shape[y - s.y]) :]
                )
            else:
                current_line = self.board[y]
            merged_rows.append(current_line)
        return "\n".join(merged_rows)


g = Game()
cycled_shapes = cycle(shapes)
i = 0
for move in cycle(movements):
    if not g.current_sprite:
        shape = next(cycled_shapes)
        if i == 2022:
            break
        i += 1
        g.place_item(shape)
    g.push(move)
    g.fall()

part1 = g.height()
print(f"Part1: {part1}")
