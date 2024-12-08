import itertools


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    for line in data.splitlines(keepends=False):
        result, operands = line.split(": ")
        result = int(result)
        operands = list(map(int, operands.split()))

        for operators in itertools.product(["+", "*"], repeat=len(operands) - 1):
            computed_result = operands[0]
            for operator, operand in zip(operators, operands[1:]):
                if operator == "+":
                    computed_result += operand
                else:
                    computed_result *= operand

            if computed_result == result:
                answer_a += result
                break

    return answer_a, None
