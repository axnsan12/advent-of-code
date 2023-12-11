import itertools

import numpy as np


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = []
    for ln in data.splitlines():
        ln = ln.strip()
        if not ln:
            continue

        ln = list(ln)
        grid.append(ln)
        if all(c == '.' for c in ln):
            # space dilation
            grid.append(ln)

    grid = np.transpose(grid)
    dilated_grid = []
    for ln in grid:
        ln = list(ln)
        dilated_grid.append(ln)
        if all(c == '.' for c in ln):
            # space dilation for columns
            dilated_grid.append(ln)

    grid = np.transpose(dilated_grid)
    nodes = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']

    answer_a = 0
    for a, b in itertools.combinations(nodes, 2):
        dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
        answer_a += dist

    return answer_a, None
