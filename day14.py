from pathlib import Path
import re


class Field:
    def __init__(self, f: str, limited=True):
        self.limited = limited
        self._entries = {0: {500: "+"}}
        for line in Path(f).read_text().splitlines():
            col_tuples = [
                (int(ss[0]), int(ss[1]))
                for s in re.split(" *-> *", line)
                if (ss := s.split(","))
            ]
            drawings = zip(col_tuples, col_tuples[1:])
            for ((x1, y1), (x2, y2)) in drawings:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        self._entries[y] = self._entries.get(y, {})
                        self._entries[y][x] = "#"

            self.max_y = max(self._entries.keys()) + (0 if self.limited else 1)

    def min_x(self):
        return min(k for d in self._entries.values() for k in d.keys())

    def max_x(self):
        return max(k for d in self._entries.values() for k in d.keys())

    def set(self, y: int, x: int, c: str):
        row = self._entries.get(y, {})
        self._entries[y] = row
        row[x] = c

    def get(self, y: int, x: int):
        return self._entries.get(y, {}).get(x, ".")

    def free(self, y: int, x: int) -> bool:
        if not self.limited and y > self.max_y:
            return False
        return self.get(y, x) == "."

    def __str__(self):
        ret = ""
        for y in range(min(self._entries.keys()), self.max_y + 1):
            ret += "".join(
                [self.get(y, x) for x in range(self.min_x(), self.max_x() + 1)]
            )
            ret += "\n"
        return ret

    def sand(self, y=1, x=500):
        if self.limited and (x < self.min_x() or x > self.max_x()):
            return False
        while self.free(y, x):
            y += 1
        if self.free(y, x - 1):
            return self.sand(y, x - 1)
        if self.free(y, x + 1):
            return self.sand(y, x + 1)
        if self.get(y - 1, x) == "o":  # Already full
            return False
        self.set(y - 1, x, "o")
        return True


for p, limited in (1, True), (2, False):
    f = Field("input14.txt", limited)
    count = 0
    while f.sand():
        count += 1
    print(f"Part{p}: {count}")
