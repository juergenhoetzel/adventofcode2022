from pathlib import Path
from operator import add, mul, floordiv, sub
import time

lines = Path("input21.txt").read_text().splitlines()
monkeys = {}
for line in lines:
    match line.split():
        case [nameq, name1, ops, name2]:
            monkeys[nameq[:-1]] = (name1, ops, name2)
        case [nameq, s]:
            monkeys[nameq[:-1]] = int(s)
        case _:
            raise ValueError(f"Invalid line: {line}")

OPSMAP = {"+": add, "*": mul, "/": floordiv, "-": sub}


def yell(monkey, opsmap=OPSMAP):
    match monkeys.get(monkey):
        case (name1, op, name2):
            return OPSMAP[op](yell(name1), yell(name2))
        case n:
            return n


print(f"Part1: {yell('root')}")
# FIXME: Don't change constant
OPSMAP["="] = lambda x, y: (x, y)
monkeys["root"] = (monkeys["root"][0], "=", monkeys["root"][2])

# binary search
low, high = 0, 2**64
while True:
    pivot = (low + high) // 2
    monkeys["humn"] = pivot
    l, r = yell("root")
    print(l, r, pivot, l - r)
    if l == r:
        break
    if l < r:
        high = pivot
    else:
        low = pivot
print(f"Part2: {pivot}")
