from __future__ import annotations
import time
import re
from functools import cmp_to_key

import numpy as np


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
        return f'<V: {self.id}, r={self.flow_rate}, {set(v.id for v in self.dsts)}>'


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
            new_dsts.add(valves[valve_id])
        valve.dsts = new_dsts

    return valves


mem = dict()


def helper(valve, score, time, open_valves):
    if time <= 0:
        return score

    state = (valve, score, time, tuple(open_valves))
    if state in mem:
        return mem[state]

    # don't open valve
    for dst in valve.dsts:
        # walk to new valve
        new_score = helper(dst, score, time - 1, open_valves)
        score = max(score, new_score)

    # open valve
    time -= 1  # time to open valve
    if time > 0:
        for dst in valve.dsts:
            if dst.flow_rate > 0 and not valve.open:
                # walk to new valve
                valve.open = True
                open_valves.add(valve.id)
                new_score = helper(dst, score + time * dst.flow_rate, time - 1, open_valves)
                open_valves.remove(valve.id)
                valve.open = False
                score = max(score, new_score)
    mem[state] = score
    return score


def main(test):
    valves = get_input(test)
    score = helper(valve=valves['AA'], score=0, time=30, open_valves = set())
    print(score)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    # main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
