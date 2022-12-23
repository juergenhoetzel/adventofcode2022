from pathlib import Path
import re


COMMANDS_RE = re.compile("([0-9]+|[RL])")
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Game:
    col: int
    row: int
    grid: list[str]
    commands: list[str | int]
    dir_index: int

    def __init__(self, path: Path):
        lines = path.read_text().splitlines()
        self.grid = lines[:-2]
        # ensure all lines have same length
        m = max([len(line) for line in self.grid])
        self.grid = [line.ljust(m) for line in self.grid]
        commands_s = lines[-1]
        self.commands = [int(token) if token.isdigit() else token for token in COMMANDS_RE.findall(commands_s)]
        self.col = self.start_col(0)
        self.row = 0
        self.dir_index = 0

    def start_col(self, y):
        return min(self.grid[y].index("."), self.grid[y].index("#"))

    def end_col(self, y):
        r_col = self.grid[y][::-1]
        return len(r_col) - 1 - min(r_col.index("."), r_col.index("#"))

    def start_row(self, x):
        column = [row[x] for row in self.grid]
        return min(column.index("."), column.index("#") if "#" in column else 1000)

    def end_row(self, x):
        r_column = [row[x] for row in self.grid][::-1]
        return len(r_column) - 1 - min(r_column.index("."), r_column.index("#") if "#" in r_column else 1000)

    def __str__(self):
        return f"""
        {self.col}
        {self.row}
""" + "\n".join(
            self.grid
        )

    def move(self) -> bool:
        d = DIRECTIONS[self.dir_index]
        if d[0]:  # move row
            new_row = self.row + d[0]
            if new_row > self.end_row(self.col):
                new_row = self.start_row(self.col)
            elif new_row < self.start_row(self.col):
                new_row = self.end_row(self.col)
            if self.grid[new_row][self.col] == "#":
                return False
            self.row = new_row
            return True
        elif d[1]:
            new_col = self.col + d[1]
            if new_col > self.end_col(self.row):
                new_col = self.start_col(self.row)
            elif new_col < self.start_col(self.row):
                new_col = self.end_col(self.row)
            if self.grid[self.row][new_col] == "#":
                return False
            self.col = new_col
            return True

    def start(self) -> int:
        for command in self.commands:
            match command:
                case int(command):
                    while command > 0 and self.move():
                        command -= 1
                case "R":
                    self.dir_index = (self.dir_index + 1) % len(DIRECTIONS)  # turn
                case "L":
                    self.dir_index = (self.dir_index - 1) % len(DIRECTIONS)  # turn
        return (self.row + 1) * 1000 + 4 * (self.col + 1) + self.dir_index


game = Game(Path("input22.txt"))
print(f"Part1: {game.start()}")
