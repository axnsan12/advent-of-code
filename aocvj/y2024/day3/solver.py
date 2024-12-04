import re


def solve(data: str) -> tuple[int | str, int | str | None]:
    mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    answer_a = sum(int(x) * int(y) for x, y in mul_re.findall(data))
    return answer_a, None
