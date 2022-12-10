from pathlib import Path

lines = Path("input10.txt").read_text().splitlines()

cycle = 1
r = 1
strengths = {}
positions = {}
for line in lines:
    cmd = line.split()
    strengths[cycle] = r * cycle
    positions[cycle] = r
    if cmd[0] == "addx":
        n = int(cmd[1])
        strengths[cycle + 1] = r * (cycle + 1)
        positions[cycle + 1] = r
        r += n
        strengths[cycle + 2] = r * (cycle + 2)
        positions[cycle + 2] = r
        cycle += 2
    elif cmd[0] == "noop":
        cycle += 1
offsets = [20, 60, 100, 140, 180, 220]
print(f"Part1: {sum([strengths[offset] for offset in offsets])}")

print("Part2:")
for i in range(1, 241):
    if i % 40 == 1:
        print()
    pos = positions[i]
    if i % 40 in (pos + 1, pos + 2, pos):
        print("#", end="")
    else:
        print(".", end="")
