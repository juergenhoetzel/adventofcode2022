from pathlib import Path


line = Path("input6.txt").read_text().splitlines()[0]
for p, n in ((1, 4), (2, 14)):
    offset = [len(set(line[i : i + n])) for i in range(len(line) - n)].index(n)
    print(f"Part{p}: {offset+n}")
