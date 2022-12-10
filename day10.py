from pathlib import Path

lines = Path("input10.txt").read_text().splitlines()

cycle = 1
r = 1
strengths = {}
for line in lines:
    cmd = line.split()
    strengths[cycle] = r * cycle
    if cmd[0] == "addx":
        n = int(cmd[1])
        strengths[cycle + 1] = r * (cycle + 1)
        r += n
        strengths[cycle + 2] = r * (cycle + 2)
        cycle += 2
    elif cmd[0] == "noop":
        cycle += 1
offsets = [20, 60, 100, 140, 180, 220]
print(f"Part1: {sum([strengths[offset] for offset in offsets])}")
