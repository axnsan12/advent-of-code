import functools
import itertools
import math

from tqdm import tqdm


@functools.lru_cache(maxsize=None)  # cache doing a lot of heavy lifting!
def solve_one(springs: str, nums: tuple[int, ...]) -> int:
    if not nums:
        # base case - no more groups to place
        if '#' in springs:
            # invalid placement because there are leftover springs
            return 0

        return 1

    # there must always be at least one empty space between each spring
    # the first group of springs must end before `reserved_space`
    reserved_space = sum(nums[1:]) + len(nums)

    total = 0
    for i in range(len(springs) - reserved_space - nums[0] + 1):
        # try to place the first group at every index
        if '.' in springs[i:i + nums[0]]:
            # cannot place over dot
            continue
        if springs[i + nums[0]] == '#':
            # must be followed by a dot
            continue
        if '#' in springs[:i]:
            # cannot leave unused springs behind
            continue

        # looks good! count number of ways to place the rest in the remaining space
        total += solve_one(springs[i + nums[0] + 1:], nums[1:])

    return total


def solve(data: str) -> tuple[int | str, int | str | None]:
    answer_a = 0
    answer_b = 0

    for line in tqdm(data.splitlines(keepends=False)):
        line = line.strip()
        if not line:
            continue

        springs, nums = line.split()
        springs = springs.strip()
        nums = tuple(map(int, nums.split(',')))

        answer_a += solve_one(springs + '.', nums)

        springs = '?'.join([springs] * 5)
        nums *= 5

        answer_b += solve_one(springs + '.', nums)

    return answer_a, answer_b
