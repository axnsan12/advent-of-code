from itertools import pairwise


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0

    for line in data.splitlines():
        numbers = [int(n) for n in line.split()]
        layers = [numbers]
        while any(layers[-1]):
            next_layer = [b - a for a, b in pairwise(layers[-1])]
            layers.append(next_layer)

        prediction = sum(layer[-1] for layer in layers)
        answer_a += prediction
    return answer_a, None
