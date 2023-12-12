import itertools

from tqdm import tqdm


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    for line in tqdm(data.splitlines(keepends=False)):
        line = line.strip()
        if not line:
            continue

        springs, nums = line.split()
        springs = list(springs.strip() + '.')
        nums = list(map(int, nums.split(',')))

        possible = []
        for idx, c in enumerate(springs):
            if c == '?':
                possible.append(((idx, '.'), (idx, '#')))

        line_answer = 0
        for plan in tqdm(itertools.product(*possible), leave=False):
            for idx, c in plan:
                springs[idx] = c

            check = []
            current = 0
            for c in springs:
                if c == '#':
                    current += 1
                elif c == '.':
                    if current > 0:
                        check.append(current)
                        current = 0
                else:
                    raise AssertionError(f'??? {c}')

            # tqdm.write(f'{springs} {check} {nums}')
            if check == nums:
                line_answer += 1

        answer_a += line_answer
        # break

    return answer_a, None
