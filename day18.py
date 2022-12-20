from pathlib import Path

cubes = {
    tuple([int(c) for c in line.split(",")])
    for line in Path("input18.txt").read_text().strip().splitlines()
}
total_sides = 0
for cube in cubes:
    x, y, z = cube
    sides = 0
    for i1, i2, i3 in (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ):
        if (x + i1, y + i2, z + i3) not in cubes:
            sides += 1
    total_sides += sides

print(total_sides)
