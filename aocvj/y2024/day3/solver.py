import re


def solve(data: str) -> tuple[int | str, int | str | None]:
    mul_re = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")
    answer_a = 0
    answer_b = 0
    dont = False
    for op in mul_re.finditer(data):
        if op.group(0) == "do()":
            dont = False
        elif op.group(0) == "don't()":
            dont = True
        else:
            x, y = map(int, op.groups())
            answer_a += x * y
            if not dont:
                answer_b += x * y
    return answer_a, answer_b
