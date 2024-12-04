DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (-1, -1), (1, -1), (-1, 1),
]


def check_xmas(grid: list[str], row: int, col: int, direction: tuple[int, int]) -> bool:
    xmas = "XMAS"
    for idx in range(len(xmas)):
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[row]):
            return False
        if grid[row][col] != xmas[idx]:
            return False

        row += direction[0]
        col += direction[1]

    return True


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = data.splitlines(keepends=False)
    answer_a = 0
    for row in range(len(grid)):
        print(grid[row])
        for col in range(len(grid[row])):
            if grid[row][col] == "X":
                for direction in DIRECTIONS:
                    if check_xmas(grid, row, col, direction):
                        answer_a += 1
    return answer_a, None
