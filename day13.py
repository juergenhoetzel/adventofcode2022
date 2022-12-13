from pathlib import Path
from functools import cmp_to_key
import ast

line_pairs = [lines.split() for lines in Path("input13.txt").read_text().split("\n\n")]

input_pairs = [(ast.literal_eval(a), ast.literal_eval(b)) for a, b in line_pairs]

first_pair = input_pairs[0]


def compare(a, b):
    if type(a) is int and type(b) is int:
        return a - b
    if type(a) is int:
        return compare([a], b)
    if type(b) is int:
        return compare(a, [b])
    for x, y in zip(a, b):
        if r := compare(x, y):
            return r
    return len(a) - len(b)


s = sum((i + 1 for i, pair in enumerate(input_pairs) if compare(*pair) < 0))
print(f"Part1: {s}")

DIVIDERS = [[[2]], [[6]]]
all_signals = [p for pair in input_pairs for p in pair] + DIVIDERS
sorted_signals = sorted(all_signals, key=cmp_to_key(compare))

s = (sorted_signals.index(DIVIDERS[0]) + 1) * (sorted_signals.index(DIVIDERS[1]) + 1)
print(f"Part2: {s}")
