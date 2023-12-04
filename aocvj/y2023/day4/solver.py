from collections import defaultdict


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    answer_b = 0

    card_copies = defaultdict(int)
    for (idx, line) in enumerate(data.splitlines(), start=1):
        numbers = line.split(':')
        winners, numbers = numbers[1].split('|')
        winners = {int(x) for x in winners.split() if x}
        numbers = [int(x) for x in numbers.split() if x]

        numbers_winning = [x for x in numbers if x in winners]
        if numbers_winning:
            answer_a += 2 ** (len(numbers_winning) - 1)

        num_copies = card_copies[idx] + 1
        for n in range(len(numbers_winning)):
            card_copies[idx + n + 1] += num_copies

        answer_b += num_copies

    return answer_a, answer_b
