import dataclasses
import functools
import heapq
from typing import Callable

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
    facing: int | None  # one of LEFT, UP, RIGHT, DOWN, or None at the start
    straight: int  # number of times we are allowed to go straight
    min_straight: int  # number of times we are *required* to go straight


def get_neighbors(grid: list[list[int]], node: Node,
                  turn_restrictions=tuple[int, int]) -> list[Node]:
    neighbors = []
    for direction in DIRECTIONS:
        if direction == node.facing and node.straight <= 0:
            # ran out of straight moves
            continue
        if direction != node.facing and node.min_straight > 0:
            # cannot turn yet
            continue
        if node.facing is not None and direction == OPPOSITES[node.facing]:
            # cannot go backwards
            continue

        delta_row, delta_col = DELTAS[direction]
        row = node.row + delta_row
        col = node.col + delta_col
        if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
            continue

        if direction == node.facing:
            straight = node.straight - 1
            min_straight = max(0, node.min_straight - 1)
        else:
            min_straight, straight = turn_restrictions
            # after a turn, we need to make sure we have enough space for min_straight tiles
            # e.g. if we are turning to facing up, min_straight is 4, but we are 3 from the top edge,
            #  then we cannot actually turn up
            far_row = node.row + min_straight * delta_row
            far_col = node.col + min_straight * delta_col
            if not (0 <= far_row < len(grid) and 0 <= far_col < len(grid[0])):
                continue

            min_straight -= 1
            straight -= 1

        neighbors.append(Node(row, col,
                              facing=direction, min_straight=min_straight, straight=straight))

    return neighbors


def get_cost(grid: list[list[int]], node: Node) -> int:
    return grid[node.row][node.col]


def dijkstra(grid: list[list[int]], start: Node,
             neighbors_func: Callable[[list[list[int]], Node], list[Node]]) -> list[list[int]]:
    visited = set()
    distances = {start: 0}
    queue = [(0, 0, start)]
    tiebreak = 1
    while queue:
        dist, _, node = heapq.heappop(queue)
        visited.add(node)

        for neighbor in neighbors_func(grid, node):
            if neighbor in visited:
                continue

            cost = dist + get_cost(grid, neighbor)
            if neighbor in distances and cost >= distances[neighbor]:
                continue

            heapq.heappush(queue, (cost, tiebreak, neighbor))
            tiebreak += 1
            distances[neighbor] = cost

    min_cost_grid: list[list[int | None]] = [[None] * len(grid[0]) for _ in range(len(grid))]
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

    start = Node(0, 0, facing=None, min_straight=0, straight=0)
    neighbors_fn_a = functools.partial(get_neighbors, turn_restrictions=(0, 3))
    answer_a = dijkstra(grid, start, neighbors_fn_a)[-1][-1]

    neighbors_fn_b = functools.partial(get_neighbors, turn_restrictions=(4, 10))
    answer_b = dijkstra(grid, start, neighbors_fn_b)[-1][-1]
    return answer_a, answer_b
