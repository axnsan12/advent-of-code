from collections import Counter

CARD_RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_RANKS = {r: i for i, r in enumerate(CARD_RANKS)}

CARD_RANKS_WITH_JOKER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
CARD_RANKS_WITH_JOKER = {r: i for i, r in enumerate(CARD_RANKS_WITH_JOKER)}


def hand_rank(hand: str, *, with_joker=False) -> int:
    if with_joker:
        return min(hand_rank(hand.replace('J', r), with_joker=False) for r in CARD_RANKS)

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


def tie_breaker(hand: str, *, with_joker=False):
    if with_joker:
        return tuple(CARD_RANKS_WITH_JOKER[c] for c in hand)
    return tuple(CARD_RANKS[c] for c in hand)


def compute_winnings(hand_bids: list[tuple[str, int]], *, with_joker: bool):
    def key_fn(hb: tuple[str, int]):
        return hand_rank(hb[0], with_joker=with_joker), tie_breaker(hb[0], with_joker=with_joker)

    hand_bids.sort(key=key_fn)
    hand_bids.reverse()

    total = 0
    for (idx, (hand, bid)) in enumerate(hand_bids, start=1):
        total += bid * idx

    return total


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = data.splitlines(keepends=False)
    hand_bids = [ln.split() for ln in lines if ln.strip()]
    hand_bids = [(h, int(b)) for (h, b) in hand_bids]

    answer_a = compute_winnings(hand_bids, with_joker=False)
    answer_b = compute_winnings(hand_bids, with_joker=True)
    return answer_a, answer_b
