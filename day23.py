from itertools import cycle, islice
from operator import attrgetter
from pathlib import Path


class Elf:
    x: int
    y: int

    def __init__(self, y, x):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Elf({self.y, self.x})"

    def position(self):
        return (self.y, self.x)


class Game:
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]

    def __init__(self, file="input.txt"):
        lines = Path(file).read_text().splitlines()
        self.elfs = [Elf(y, x) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"]
        self.looking_positions = cycle([(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1)])

    def try_move(self, elf, check_positions, elf_positions) -> None | tuple[int, int]:
        final_pos = (elf.y + check_positions[1][0], (elf.x + check_positions[1][1]))
        is_occupied = any((elf.y + off_y, elf.x + off_x) in elf_positions for off_y, off_x in check_positions)
        if not is_occupied:
            return final_pos

    def is_elf_around(self, elf, elf_positions):
        return any([(elf.y + off_y, elf.x + off_x) in elf_positions for off_y, off_x in Game.DIRECTIONS])

    def rect_size(self):
        y_min = min(self.elfs, key=attrgetter("y")).y
        y_max = max(self.elfs, key=attrgetter("y")).y
        x_min = min(self.elfs, key=attrgetter("x")).x
        x_max = max(self.elfs, key=attrgetter("x")).x
        return (y_max - y_min + 1) * (x_max - x_min + 1) - len(self.elfs)

    def move(self) -> int:
        elf_positions = {elf.position() for elf in self.elfs}
        moves = {}
        for _ in range(4):  # all directions
            check_positions = list(islice(self.looking_positions, 3))
            for elf in self.elfs:
                if (self.is_elf_around(elf, elf_positions)) and (elf not in moves) and (new_pos := self.try_move(elf, check_positions, elf_positions)):
                    moves[elf] = new_pos
        new_positions = list(moves.values())
        for elf, (new_y, new_x) in moves.items():
            if new_positions.count((new_y, new_x)) == 1:  # not crowded
                elf.y = new_y
                elf.x = new_x
        list(islice(self.looking_positions, 3))  # start in next direction next round
        return len(new_positions)


if __name__ == "__main__":
    g = Game("input23.txt")
    for _ in range(10):
        g.move()
    print(f"Part1: {g.rect_size()}")
    g = Game("input23.txt")
    count = 1
    while g.move():
        count += 1
    print(f"Part2: {count}")
