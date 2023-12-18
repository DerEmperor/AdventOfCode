#!/usr/bin/env python
from __future__ import annotations

import re
import time
from functools import cached_property
from itertools import groupby, cycle
from math import lcm
from typing import List

data_re = re.compile(r'(\S+) = \((\S+), (\S+)\)\n')
RL = {'L': 0, 'R': 1}


def get_input(test: bool):
    data = {}
    filename = 'inputs/08_test.txt' if test else 'inputs/08.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        rl = input_[0][:-1]
        for line in input_[2:]:
            key, r, l = data_re.match(line).groups()
            data[key] = (r, l)

    return rl, data


def main(test: bool):
    rls, data = get_input(test)
    pos1 = 'AAA'
    cnt1 = 0
    for rl in cycle(rls):
        if pos1 == 'ZZZ':
            break
        cnt1 += 1
        pos1 = data[pos1][RL[rl]]
    print(cnt1)

    pos2 = []
    for pos in data.keys():
        if pos[-1] == 'A':
            pos2.append(pos)
    cnt2 = []
    for p in pos2:
        c = 0
        for rl in cycle(rls):
            if p[-1] == 'Z':
                cnt2.append(c)
                break
            c += 1
            p = data[p][RL[rl]]

    print(lcm(*cnt2))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
