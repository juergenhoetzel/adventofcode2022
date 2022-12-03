from pathlib import Path


def priority(c):
    if c.isupper():
        return ord(c) - ord("A") + 27
    return ord(c) - ord("a") + 1


part1 = sum(
    [
        priority(*(set(line[:s]) & set(line[s:])))  # should be exactile one
        for line in Path("input3.txt").read_text().splitlines()
        if (s := len(line) // 2)
    ]
)
print(f"Part1: {part1}")

lines = [
    line
    for line in Path("input3.txt").read_text().splitlines()
    if (s := len(line) // 2)
]


part2 = sum(
    [
        priority(*set.intersection(*[set(sack) for sack in lines[i : (i + 3)]]))
        for i in range(0, len(lines), 3)
    ]
)


print(f"Part2: {part2}")
