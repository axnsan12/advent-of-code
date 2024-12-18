import itertools
from collections import defaultdict


def grid_set(grid, row, col, value):
    if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
        grid[row][col] = value
        return True

    return False


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = [list(row) for row in data.splitlines(keepends=False)]
    antennas_by_type = defaultdict(list)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != '.':
                antennas_by_type[grid[row][col]].append((row, col))

    antinodes_a = set()
    antinodes_b = set()
    for antenna_type, antennas in antennas_by_type.items():
        for a, b in itertools.combinations(antennas, 2):
            row_d = a[0] - b[0]
            col_d = a[1] - b[1]
            antinodes_a.add((a[0] + row_d, a[1] + col_d))
            antinodes_a.add((b[0] - row_d, b[1] - col_d))

            for sign in (-1, 1):
                row, col = a
                while grid_set(grid, row, col, '#'):
                    antinodes_b.add((row, col))
                    row += sign * row_d
                    col += sign * col_d

    answer_a = 0
    for row, col in antinodes_a:
        answer_a += grid_set(grid, row, col, '#')
    return answer_a, len(antinodes_b)
