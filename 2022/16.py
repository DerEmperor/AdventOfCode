from __future__ import annotations

import functools
import itertools
import time
import re
from collections import defaultdict


class Valve:
    def __init__(self, id, flow_rate, dsts):
        self.id = id
        self.flow_rate = flow_rate
        self.dsts = dsts
        self.open = False

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'<V: {self.id}, r={self.flow_rate}, {set((v.id, d) for v, d in self.dsts)}>'


def get_input(test):
    filename = 'inputs/16_test.txt' if test else 'inputs/16.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()

    line_regex = re.compile(
        r'Valve ([a-zA-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ((?:[a-zA-Z]{2}(?:, )?)*)\n',
    )
    valves = dict()
    for line in input_:
        id, flow_rate, dsts = line_regex.match(line).groups()
        valves[id] = Valve(id, int(flow_rate), dsts.split(', '))

    # replace dst by valve
    for valve in valves.values():
        new_dsts = set()
        for valve_id in valve.dsts:
            new_dsts.add((valves[valve_id], 1))
        valve.dsts = new_dsts

    return valves


def floyd_warshall(valves):
    distances = defaultdict(lambda: len(valves) + 1)
    for valve in valves.values():
        for valve2, dis in valve.dsts:
            distances[valve.id, valve2.id] = dis
            distances[valve2.id, valve.id] = dis
        valve.dsts.clear()
    for k, i, j in itertools.product([v.id for v in valves.values()], repeat=3):
        distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])

    for (v_id, v2_id), dis in distances.items():
        v = valves[v_id]
        v2 = valves[v2_id]
        if (v.flow_rate > 0 or v_id == 'AA') and v2.flow_rate > 0 and v_id != v2_id:
            v.dsts.add((v2, dis))

    # throw away valves with flow rate 0
    for valve in list(valves.values()):
        if valve.flow_rate == 0 and valve.id != 'AA':
            del valves[valve.id]


def part1(valve, time_left):
    if time_left <= 0 or valve.open:
        return 0

    score = 0

    for dst, dis in valve.dsts:
        # walk to new valve
        valve.open = True
        score = max(score, part1(dst, time_left - dis - (1 if valve.flow_rate > 0 else 0)) + (time_left - 1) * valve.flow_rate)
        valve.open = False

    return score


@functools.cache
def part2(start_valve, valve, open_valves, time_left, foo):
    if time_left <= 0 or valve.id not in open_valves:
        return 0

    score = 0

    for dst, dis in valve.dsts:
        # walk to new valve
        res = part2(start_valve, dst, open_valves - {valve.id}, time_left - dis - (1 if valve.flow_rate > 0 else 0), foo)
        res += (time_left - 1) * valve.flow_rate
        score = max(score, res)
    if foo:
        res = part2(start_valve, start_valve, open_valves | {'AA'}, 26, False)
        score = max(score, res)
    return score


def main(test):
    valves = get_input(test)
    floyd_warshall(valves)
    print(part1(valves['AA'], 30))
    print(part2(valves['AA'], valves['AA'], frozenset(valves.keys()), 26, True))


if __name__ == '__main__':
    start_time = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    execution_time = (time.time() - start_time)
    print('Execution time: ' + str(round(execution_time, 3)) + ' s')
