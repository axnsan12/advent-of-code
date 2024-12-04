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


def check_x_mas(grid: list[str], row: int, col: int) -> bool:
    if not grid[row][col] == "A":
        return False
    if row <= 0 or row >= len(grid) - 1 or col <= 0 or col >= len(grid[row]) - 1:
        return False

    top_left = grid[row - 1][col - 1]
    top_right = grid[row - 1][col + 1]
    bottom_left = grid[row + 1][col - 1]
    bottom_right = grid[row + 1][col + 1]

    mas = 0
    if top_left == "M" and bottom_right == "S":
        mas += 1
    if top_right == "M" and bottom_left == "S":
        mas += 1
    if top_left == "S" and bottom_right == "M":
        mas += 1
    if top_right == "S" and bottom_left == "M":
        mas += 1

    return mas == 2


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = data.splitlines(keepends=False)
    answer_a = 0
    answer_b = 0
    for row in range(len(grid)):
        print(grid[row])
        for col in range(len(grid[row])):
            if grid[row][col] == "X":
                for direction in DIRECTIONS:
                    if check_xmas(grid, row, col, direction):
                        answer_a += 1
            if grid[row][col] == "A":
                if check_x_mas(grid, row, col):
                    answer_b += 1

    return answer_a, answer_b
