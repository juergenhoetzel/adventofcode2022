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


input_pairs = [line.split(" ") for line in Path("input2.txt").read_text().splitlines()]
print(sum([score(opponent, me) for (opponent, me) in input_pairs]))
