#!/usr/bin/env python

from __future__ import annotations

import time
from typing import List, Tuple


def get_input(test: bool):
    designs = []
    filename = 'inputs/19_test.txt' if test else 'inputs/19.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        towels = input_[0][:-1].split(', ')
        for line in input_[2:]:
            designs.append(line[:-1])
    return towels, designs


def is_possible(design: str, towels: List[str]) -> int:
    mem = {}

    def is_possible_helper(i: int) -> int:
        if i == len(design):
            return 1
        assert i < len(design)
        if i in mem:
            return mem[i]
        res = 0
        for towel in towels:
            if design.startswith(towel, i):
                res += is_possible_helper(i + len(towel))
        mem[i] = res
        return res

    return is_possible_helper(0)


def main(test: bool):
    towels, designs = get_input(test)
    part1 = 0
    part2 = 0
    for i, design in enumerate(designs):
        res = is_possible(design, towels)
        if res > 0:
            part1 += 1
        part2 += res

    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
