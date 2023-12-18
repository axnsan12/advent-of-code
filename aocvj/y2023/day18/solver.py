import numpy as np


# https://stackoverflow.com/questions/41077185/fastest-way-to-shoelace-formula
def shoelace(points):
    n = len(points)
    n_segments = n - 1

    area = [(points[i + 1][0] - points[i][0]) * (points[i + 1][1] + points[i][1])
            for i in range(n_segments)]

    return abs(sum(area) / 2.)


class Poly:
    def __init__(self):
        self.poly = [(0, 0)]
        self.perimeter = 0
        self.pos = (0, 0)

    def add(self, direction, dist):
        if direction == 'R':
            next_pos = (self.pos[0], self.pos[1] + dist)
        elif direction == 'L':
            next_pos = (self.pos[0], self.pos[1] - dist)
        elif direction == 'U':
            next_pos = (self.pos[0] - dist, self.pos[1])
        elif direction == 'D':
            next_pos = (self.pos[0] + dist, self.pos[1])
        else:
            raise ValueError(f'invalid direction {direction}')

        self.poly.append(next_pos)
        self.pos = next_pos
        self.perimeter += dist

    def area(self):
        assert len(self.poly) >= 3 and self.poly[0] == self.poly[-1], \
            f'bad poly {len(self.poly)} {self.poly}'
        return int(shoelace(self.poly)) + self.perimeter // 2 + 1


def solve(data: str) -> tuple[int | str, int | str | None]:
    poly_a = Poly()
    poly_b = Poly()

    for ln in data.splitlines():
        dir_a, dist_a, color = ln.split()
        dist_a = int(dist_a)

        dist_b = int(color[2:-2], 16)
        dir_b = "RDLU"[int(color[-2])]

        poly_a.add(dir_a, dist_a)
        poly_b.add(dir_b, dist_b)

    answer_a = poly_a.area()
    answer_b = poly_b.area()
    return answer_a, answer_b
