from pathlib import Path


def interleave_message(s, n=4):
    return zip(*[line[i:] for i in range(n)])


line = Path("input6.txt").read_text().splitlines()[0]
offs = [[len(set(xs)) for xs in interleave_message(line, n)].index(n) for n in (4, 14)]
print(f"Part1: {offs[0]+4}")
print(f"Part2: {offs[1]+14}")
