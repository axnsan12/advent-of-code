import copy
from collections import defaultdict

from tqdm import tqdm

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def find_guard(grid: list[list[str]]) -> tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "^":
                return row, col

    raise AssertionError("Guard not found")


def get_next_direction(grid: list[list[str]], row: int, col: int, direction: int) -> int | None:
    for i in range(3):
        next_row, next_col = row + DIRECTIONS[direction][0], col + DIRECTIONS[direction][1]
        if next_row < 0 or next_row >= len(grid) or next_col < 0 or next_col >= len(grid[row]):
            return None

        if grid[next_row][next_col] == "#":
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            return direction

    raise AssertionError("Dead end??")


def find_path(grid: list[list[str]], row: int, col: int) -> int | None:
    length = 0
    visited = defaultdict(list)
    direction = 0
    while True:
        length += ((row, col) not in visited)
        direction = get_next_direction(grid, row, col, direction)
        if direction is None:
            return length
        visited_directions = visited[(row, col)]
        if direction in visited_directions:
            return None
        visited_directions.append(direction)
        row, col = row + DIRECTIONS[direction][0], col + DIRECTIONS[direction][1]


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = [list(line) for line in data.splitlines(keepends=False)]
    start_row, start_col = find_guard(grid)
    answer_a = find_path(grid, start_row, start_col)
    answer_b = 0

    with tqdm(total=len(grid) * len(grid[0])) as pbar:
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                pbar.update(1)
                if grid[row][col] == '.':
                    grid[row][col] = "#"
                    length = find_path(grid, start_row, start_col)
                    answer_b += length is None
                    grid[row][col] = "."
    return answer_a, answer_b
