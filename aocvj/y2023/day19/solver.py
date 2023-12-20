import dataclasses
import operator
import re
from collections import defaultdict
from typing import Callable


@dataclasses.dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


uniq_conditions = defaultdict(set)


def parse_condition(condition: str) -> Callable[[Part], bool]:
    ops = [
        ('<', operator.lt),
        ('>', operator.gt),
    ]

    for op_str, op_fn in ops:
        if op_str in condition:
            attr_name, value = condition.split(op_str)
            value = int(value)
            uniq_conditions[attr_name].add(value)
            return lambda part: op_fn(getattr(part, attr_name), value)

    raise ValueError(f'unknown condition: {condition}')


def solve(data: str) -> tuple[int | str, int | str | None]:
    lines = iter(data.splitlines(keepends=False))

    workflows = {}  # type: dict[str, list[tuple[str, Callable[[Part], bool]]]]
    for ln in lines:
        if not ln:
            break

        state, rules = re.match(r"^(.*?)\{(.*?)}$", ln).groups()
        flow = []
        for rule in rules.split(','):
            if ':' in rule:
                condition, target = rule.split(':')
                flow.append((target, parse_condition(condition)))
            else:
                flow.append((rule, lambda _: True))

        workflows[state] = flow

    parts = []
    for ln in lines:
        attrs = {}
        for a in ln[1:-1].split(','):
            k, v = a.split('=')
            attrs[k] = int(v)

        parts.append(Part(**attrs))

    for attr_name, values in uniq_conditions.items():
        print(f'for {attr_name} there are {len(values)} uniq conditions')

    answer_a = 0
    for part in parts:
        state = 'in'
        while state not in ('A', 'R'):
            for target, condition in workflows[state]:
                if condition(part):
                    state = target
                    break
            else:
                raise AssertionError(f'{part} stuck in {state} {workflows[state]}')

        if state == 'A':
            answer_a += part.x + part.m + part.a + part.s

    return answer_a, None
