from pathlib import Path


def priority(c):
    if c.isupper():
        return ord(c) - ord("A") + 27
    return ord(c) - ord("a") + 1


print(
    sum(
        [
            priority(*(set(line[:s]) & set(line[s:])))  # should be exactile one
            for line in Path("input3.txt").read_text().splitlines()
            if (s := len(line) // 2)
        ]
    )
)
