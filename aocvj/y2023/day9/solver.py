from itertools import pairwise


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    answer_b = 0

    for line in data.splitlines():
        numbers = [int(n) for n in line.split()]
        layers = [numbers]
        while any(layers[-1]):
            next_layer = [b - a for a, b in pairwise(layers[-1])]
            layers.append(next_layer)

        answer_a += sum(layer[-1] for layer in layers)

        layers.reverse()
        prediction_prev = 0
        for layer in layers:
            prediction_prev = layer[0] - prediction_prev

        answer_b += prediction_prev
    return answer_a, answer_b
