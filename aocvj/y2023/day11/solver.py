import itertools

import numpy as np


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = []
    empty_rows = []
    empty_cols = []
    for ln in data.splitlines():
        ln = ln.strip()
        if not ln:
            continue

        grid.append(ln)

    for row in range(len(grid)):
        if all(c == '.' for c in grid[row]):
            empty_rows.append(row)

    for col in range(len(grid[0])):
        if all(grid[row][col] == '.' for row in range(len(grid))):
            empty_cols.append(col)

    nodes = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']

    answer_a = 0
    answer_b = 0
    for a, b in itertools.combinations(nodes, 2):
        er = sum(1 for r in empty_rows if a[0] < r < b[0] or b[0] < r < a[0])
        ec = sum(1 for c in empty_cols if a[1] < c < b[1] or b[1] < c < a[1])
        dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
        answer_a += dist + (er + ec) * 2 - er - ec
        answer_b += dist + (er + ec) * 1_000_000 - er - ec

    return answer_a, answer_b
