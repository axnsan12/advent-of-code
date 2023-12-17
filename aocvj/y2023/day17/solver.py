import dataclasses

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

DIRECTIONS = [LEFT, UP, RIGHT, DOWN]
OPPOSITES = [RIGHT, DOWN, LEFT, UP]
DELTAS = [(0, -1), (-1, 0), (0, 1), (1, 0)]


@dataclasses.dataclass(frozen=True)
class Node:
    row: int
    col: int
    facing: int  # one of LEFT, UP, RIGHT, DOWN
    straight: int  # number of times we are allowed to go straight


def get_neighbors(grid: list[list[int]], node: Node) -> list[Node]:
    neighbors = []
    for direction in DIRECTIONS:
        if direction == node.facing and node.straight <= 0:
            # ran out of straight moves
            continue
        if direction == OPPOSITES[node.facing]:
            # cannot go backwards
            continue

        delta_row, delta_col = DELTAS[direction]
        row = node.row + delta_row
        col = node.col + delta_col
        if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
            continue

        if direction == node.facing:
            straight = node.straight - 1
        else:
            straight = 2

        neighbors.append(Node(row, col, direction, straight))

    return neighbors


def get_cost(grid: list[list[int]], node: Node) -> int:
    return grid[node.row][node.col]


def dijkstra(grid: list[list[int]], start: Node) -> list[list[int]]:
    visited = set()
    unvisited = {start}
    distances = {start: 0}
    queue = []
    while unvisited:
        node = min(unvisited, key=distances.get)
        unvisited.remove(node)
        visited.add(node)

        for neighbor in get_neighbors(grid, node):
            if neighbor in visited:
                continue

            cost = distances[node] + get_cost(grid, neighbor)
            if neighbor not in unvisited:
                unvisited.add(neighbor)
            elif cost >= distances[neighbor]:
                continue

            distances[neighbor] = cost

    min_cost_grid = [[None] * len(grid[0]) for _ in range(len(grid))]
    for node, cost in distances.items():
        current = min_cost_grid[node.row][node.col]
        if current is None or cost < current:
            min_cost_grid[node.row][node.col] = cost

    assert all(all(e is not None for e in ln) for ln in min_cost_grid)
    return min_cost_grid


def solve(data: str) -> tuple[int | str, int | str | None]:
    grid = []
    for ln in data.splitlines(keepends=False):
        ln = ln.strip()
        if not ln:
            continue

        grid.append(list(map(int, ln)))

    start = Node(0, 0, RIGHT, 3)
    min_cost_grid = dijkstra(grid, start)
    answer_a = min_cost_grid[-1][-1]
    return answer_a, None
