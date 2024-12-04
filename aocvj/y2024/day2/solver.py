import itertools


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    for line in data.splitlines():
        numbers = list(map(int, line.split()))
        diffs = [a - b for a, b in itertools.pairwise(numbers)]
        sign = diffs[0] < 0
        if all(((v < 0) == sign) and (1 <= abs(v) <= 3) for v in diffs):
            answer_a += 1
    return answer_a, None
