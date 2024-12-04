import itertools


def is_safe(numbers: list[int]) -> bool:
    diffs = [a - b for a, b in itertools.pairwise(numbers)]
    sign = diffs[0] < 0
    return all(((v < 0) == sign) and (1 <= abs(v) <= 3) for v in diffs)


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    answer_b = 0
    for line in data.splitlines():
        numbers = list(map(int, line.split()))
        if is_safe(numbers):
            answer_a += 1
        for idx in range(len(numbers)):
            if is_safe(numbers[:idx] + numbers[idx + 1:]):
                answer_b += 1
                break
    return answer_a, answer_b
