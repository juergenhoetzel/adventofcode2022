import re
from pathlib import Path


def parse_line(line):
    f1, t1, f2, t2 = [
        int(s) for s in re.match("^([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)$", line).groups()
    ]
    return set(range(f1, t1 + 1)), set(range(f2, t2 + 1))


def is_included(s1, s2):
    return s1 & s2 in (s1, s2)


print(
    sum(
        [
            is_included(*parse_line(line))
            for line in Path("input4.txt").read_text().splitlines()
        ]
    )
)
