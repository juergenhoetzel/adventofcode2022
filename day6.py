from pathlib import Path

line = Path("input6.txt").read_text().splitlines()[0]
offset = [len(set(xs)) for xs in zip(line, line[1:], line[2:], line[3:])].index(4)
print(offset + 4)
