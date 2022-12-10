from pathlib import Path

movements = [
    (cols[0], int(cols[1]))
    for line in Path("input9.txt").read_text().splitlines()
    if (cols := line.split())
]
t_x = 0
t_y = 0
h_x = 0
h_y = 0
visited_positions = set((t_x, t_y))
for (direction, n) in movements:
    for _ in range(n):
        match direction:
            case "R":
                h_x += 1
            case "U":
                h_y -= 1
            case "D":
                h_y += 1
            case "L":
                h_x -= 1
            case _:
                raise ValueError("Invalid move: {direction}")
        dist_x = h_x - t_x
        dist_y = h_y - t_y
        match (dist_x, dist_y):
            case (2, 0):
                t_x += 1
                visited_positions.add((t_x, t_y))
            case (-2, 0):
                t_x -= 1
                visited_positions.add((t_x, t_y))
            case (2, 1) | (1, 2):
                t_x += 1
                t_y += 1
                visited_positions.add((t_x, t_y))
            case (2, -1) | (1, -2):
                t_x += 1
                t_y -= 1
                visited_positions.add((t_x, t_y))
            case (0, 2):
                t_y += 1
                visited_positions.add((t_x, t_y))
            case (0, -2):
                t_y -= 1
                visited_positions.add((t_x, t_y))
            case (-1, 2) | (-2, 1):
                t_x -= 1
                t_y += 1
                visited_positions.add((t_x, t_y))
            case (-2, -1) | (-1, -2):
                t_x -= 1
                t_y -= 1
                visited_positions.add((t_x, t_y))
            case (1, 1) | (-1, -1) | (0, 1) | (1, 0) | (0, -1) | (-1, 0) | (1, -1) | (
                0,
                0,
            ) | (
                -1,
                1,
            ):
                pass
            case _:
                raise ValueError(f"Invalid move {direction} {dist_x, dist_y}")

print(len(visited_positions))
