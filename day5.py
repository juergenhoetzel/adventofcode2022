from pathlib import Path
from dataclasses import dataclass
import re


@dataclass
class State:
    stacks: list[list[str]]

    def move(self, n: int, src: int, dst: int, reverse=True):
        items = self.stacks[src - 1][-n:]
        if reverse:
            items = reversed(items)
        self.stacks[src - 1] = self.stacks[src - 1][:-n]
        self.stacks[dst - 1] = [*self.stacks[dst - 1], *items]

    def __str__(self):
        "Top representation of stacks"
        return "".join([stack[-1] for stack in self.stacks if len(stack)])


def parse_input() -> (State, tuple[int, int, int]):
    sections = Path("input5.txt").read_text().split("\n\n")
    state_lines = sections[0].splitlines()
    crate_positions = [
        match.span()[0] for match in (re.finditer("[0-9]+", state_lines[-1]))
    ]
    stacks: list[str] = [[] for _ in range(len(crate_positions))]
    for crate_str in state_lines[:-1]:
        for offset, i in zip(crate_positions, range(len(crate_positions))):
            if len(crate_str) > offset and (c := crate_str[offset]).isalpha():
                stacks[i] = [c, *stacks[i]]
    commands = [
        [
            int(s)
            for s in re.match("move ([0-9]+) from ([0-9]+) to ([0-9+])", line).groups()
        ]
        for line in sections[1].splitlines()
    ]
    return State(stacks), commands


state, movements = parse_input()
state2 = State([*state.stacks])
for movement in movements:
    state.move(*movement)
    state2.move(*movement, False)
print(f"Part1: {state}")
print(f"Part2: {state2}")
