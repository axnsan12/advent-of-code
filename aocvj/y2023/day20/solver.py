import collections
import copy
import dataclasses
import itertools
import re
from collections import defaultdict

from tqdm import tqdm


class ModuleInterface:
    def accept_input(self, sender: str, pulse: bool) -> bool:
        raise NotImplementedError()

    def emit_pulse(self):
        raise NotImplementedError()


@dataclasses.dataclass
class Broadcaster(ModuleInterface):
    state: bool

    def accept_input(self, sender: str, pulse: bool) -> bool:
        self.state = pulse
        return True

    def emit_pulse(self):
        return self.state


@dataclasses.dataclass
class FlipFlop(ModuleInterface):
    state: bool

    def accept_input(self, sender: str, pulse: bool) -> bool:
        if not pulse:
            self.state = not self.state
            return True

        return False

    def emit_pulse(self):
        return self.state


@dataclasses.dataclass
class Conjunction(ModuleInterface):
    input_states: dict[str, bool]

    def accept_input(self, sender: str, pulse: bool) -> bool:
        self.input_states[sender] = pulse
        return True

    def emit_pulse(self):
        return False if all(self.input_states.values()) else True


@dataclasses.dataclass
class Sink(ModuleInterface):
    state: bool

    def accept_input(self, sender: str, pulse: bool) -> bool:
        self.state = pulse
        return False

    def emit_pulse(self):
        return False


@dataclasses.dataclass
class Circuit:
    modules: dict[str, ModuleInterface]
    links: dict[str, list[str]]


def parse_graph(data: str) -> Circuit:
    modules: dict[str, ModuleInterface] = {}

    links: dict[str, list[str]] = {}
    reverse_links = defaultdict(list)
    for ln in data.splitlines(keepends=False):
        ln = ln.strip()
        if not ln:
            continue

        src, dst = re.match(r'^(.*?) -> (.*?)$', ln).groups()
        if src.startswith('%'):
            src = src[1:]
            modules[src] = FlipFlop(False)
        elif src.startswith('&'):
            src = src[1:]
            modules[src] = Conjunction({})
        elif src == 'broadcaster':
            modules[src] = Broadcaster(False)

        dst = [d.strip() for d in dst.split(',')]
        links[src] = dst
        for d in dst:
            reverse_links[d].append(src)

    for node, parents in reverse_links.items():
        module = modules.get(node)
        if module is None:
            print(f'dummy module: {node}')
            modules[node] = Sink(True)
            continue
        if isinstance(module, Conjunction):
            module.input_states = {s: False for s in parents}

    return Circuit(modules, links)


def send_broadcast(circuit: Circuit):
    pulse_queue = collections.deque()
    pulse_queue.append(('button', 'broadcaster', False))

    count_low = 0
    count_high = 0
    while pulse_queue:
        # print(f'clock')
        emitters = []
        while pulse_queue:
            src, target, pulse = pulse_queue.popleft()
            if pulse:
                count_high += 1
            else:
                count_low += 1
            # print(f'{src} -{"high" if pulse else "low"}-> {target}')
            module = circuit.modules[target]
            if module.accept_input(src, pulse):
                emitters.append(target)

        for emitter in emitters:
            for target in circuit.links[emitter]:
                module = circuit.modules[emitter]
                pulse = module.emit_pulse()

                pulse_queue.append((emitter, target, pulse))

    return count_low, count_high


def solve(data: str) -> tuple[int | str, int | str | None]:
    circuit_orig = parse_graph(data)

    circuit_a = copy.deepcopy(circuit_orig)
    total_low = 0
    total_high = 0
    for _ in range(1000):
        low, high = send_broadcast(circuit_a)
        total_low += low
        total_high += high

    answer_a = total_low * total_high

    answer_b = 0
    circuit_b = copy.deepcopy(circuit_orig)
    rx = circuit_b.modules.get('rx') or circuit_b.modules.get('output')
    if rx is not None:
        assert isinstance(rx, Sink)

        for idx in tqdm(itertools.count(1)):
            send_broadcast(circuit_b)

            if rx.state:
                continue

            answer_b = idx
            break

    return answer_a, answer_b
