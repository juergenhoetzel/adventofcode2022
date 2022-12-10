from pathlib import Path

grid = [[int(c) for c in line] for line in Path("input8.txt").read_text().splitlines()]


def visible_nodes(grid):
    nodes = []
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            height = grid[y][x]
            inv_y_t = any((grid[y1][x] >= height for y1 in range(0, y)))
            inv_y_b = any((grid[y1][x] >= height for y1 in range(y + 1, len(grid))))
            inv_x_l = any((grid[y][x1] >= height for x1 in range(0, x)))
            inv_x_r = any((grid[y][x1] >= height for x1 in range(x + 1, len(grid[y]))))
            visible = not all(
                [
                    inv_y_b,
                    inv_y_t,
                    inv_x_r,
                    inv_x_l,
                ]
            )
            if visible:
                nodes.append((y, x, height, visible))
    return nodes


n = len(visible_nodes(grid)) + len(grid) * 4 - 4
print(f"Part1: {n}")
