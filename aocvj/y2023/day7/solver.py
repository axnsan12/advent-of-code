from collections import Counter

CARD_RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_RANKS = {r: i for i, r in enumerate(CARD_RANKS)}


def hand_rank(hand: str) -> int:
    counts = Counter(hand)
    counts_per_rank = counts.most_common(5)
    if len(counts_per_rank) == 1:
        # 5 of a kind
        return 0
    if len(counts_per_rank) == 2:
        if counts_per_rank[0][1] == 4:
            # 4 of a kind
            return 1
        if counts_per_rank[0][1] == 3:
            # full house
            return 2

        raise AssertionError(f'unreachable, {counts=} {hand=}')
    if len(counts_per_rank) == 3:
        if counts_per_rank[0][1] == 3:
            # 3 of a kind
            return 3
        if counts_per_rank[0][1] == 2:
            # 2 pairs
            return 4

        raise AssertionError(f'unreachable, {counts=} {hand=}')
    if len(counts_per_rank) == 4:
        # 1 pair
        return 5

    # high card
    return 6


def tie_breaker(hand: str):
    return tuple(CARD_RANKS[c] for c in hand)


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    hand_bids = [ln.split() for ln in lines]
    hand_bids.sort(key=lambda x: (hand_rank(x[0]), tie_breaker(x[0])))
    hand_bids.reverse()

    answer_a = 0
    for (idx, (hand, bid)) in enumerate(hand_bids, start=1):
        answer_a += int(bid) * idx

    return answer_a, None
