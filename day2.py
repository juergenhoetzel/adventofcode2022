from pathlib import Path

SCORES = {
    "A": {"Y": 6, "X": 3, "Z": 0},
    "B": {"Y": 3, "X": 0, "Z": 6},
    "C": {"Y": 0, "X": 6, "Z": 3},
}


def points(c):
    return ord(c) - ord("X") + 1


def score(opponent, me):
    return SCORES[opponent][me] + points(me)


SCORES2 = {
    "A": {"Y": 1 + 3, "X": 3 + 0, "Z": 2 + 6},
    "B": {"Y": 2 + 3, "X": 1 + 0, "Z": 3 + 6},
    "C": {"Y": 3 + 3, "X": 2 + 0, "Z": 1 + 6},
}


input_pairs = [line.split(" ") for line in Path("input2.txt").read_text().splitlines()]
part1 = sum([score(opponent, me) for (opponent, me) in input_pairs])
part2 = sum([SCORES2[opponent][strategy] for (opponent, strategy) in input_pairs])
print(f"Part1: {part1}")
print(f"Part2: {part2}")
