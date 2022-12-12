import re
from dataclasses import dataclass
from functools import reduce
from operator import add, mul
from pathlib import Path


@dataclass
class Monkey:
    n: int
    items: list[int]
    operation: str
    x: str
    mod: int
    monkey1: int
    monkey2: int
    inspections: int = 0

    def inspect(self, monkeys: list[Monkey], mod=None):
        for item in self.items:
            self.inspections += 1
            if self.operation == "*":
                op = mul
            else:
                op = add
            if self.x == "old":
                item = op(item, item)
            else:
                item = op(item, int(self.x))

            if mod:
                item = item % mod
            else:
                item = item // 3
            if item % self.mod == 0:
                monkeys[self.monkey1].items.append(item)
            else:
                monkeys[self.monkey2].items.append(item)
        self.items = []


monkey_strs = [
    part.strip()
    for part in re.split(r"^$", Path("input11.txt").read_text(), flags=re.MULTILINE)
]


def parse_monkey(s: str):
    (n, items_str, op, x, mod, monkey1, monkey2) = re.match(
        """Monkey ([0-9]):
 *Starting items: ([0-9, ]+)
 *Operation: new = old (.) (.+)
 *Test: divisible by ([0-9]+)
 *If true: throw to monkey ([0-9]+)
 *If false: throw to monkey ([0-9]+)""",
        s.strip(),
        flags=re.MULTILINE,
    ).groups()
    return Monkey(
        int(n),
        [int(s) for s in items_str.split(", ")],
        op,
        x,
        int(mod),
        int(monkey1),
        int(monkey2),
    )


def parse_monkeys(monkey_strs):
    return [
        parse_monkey(monkey_str)
        for monkey_str in monkey_strs
        if monkey_str.startswith("Monkey")
    ]


monkeys = parse_monkeys(monkey_strs)


def interact(times: int, mod=None):
    for i in range(times):
        for monkey in monkeys:
            monkey.inspect(monkeys, mod)


interact(20)
i1, i2 = sorted(monkey.inspections for monkey in monkeys)[-2:]
print(f"Part1:  {i1*i2}")

monkeys = parse_monkeys(monkey_strs)

mod = reduce(mul, [monkey.mod for monkey in monkeys])
interact(10000, mod)
i1, i2 = sorted(monkey.inspections for monkey in monkeys)[-2:]
print(f"Part2:  {i1*i2}")
