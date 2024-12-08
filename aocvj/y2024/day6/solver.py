import copy

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


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = [list(line) for line in data.splitlines(keepends=False)]
    row, col = find_guard(grid)
    direction = 0
    answer_a = 0
    while True:
        answer_a += (grid[row][col] != 'X')
        grid[row][col] = 'X'
        direction = get_next_direction(grid, row, col, direction)
        if direction is None:
            break
        row, col = row + DIRECTIONS[direction][0], col + DIRECTIONS[direction][1]

    return answer_a, None
