#!/usr/bin/env python
from __future__ import annotations

import time
from collections import defaultdict
from typing import Tuple, Set


class Pos:
    dimensions: Tuple[int, int] | None = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: Pos):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos):
        return Pos(self.x - other.x, self.y - other.y)

    def in_bounds(self) -> bool:
        assert self.dimensions is not None
        return 0 <= self.x < self.dimensions[0] and 0 <= self.y < self.dimensions[1]

    def get_antinodes_1(self, other: Pos) -> Tuple[Pos, Pos]:
        p1 = Pos(2 * self.x - other.x, 2 * self.y - other.y)
        p2 = Pos(2 * other.x - self.x, 2 * other.y - self.y)
        return p1, p2

    def get_antinodes_2(self, other: Pos) -> Set[Pos]:
        res = set()
        i = 0
        while True:
            p = Pos((i + 1) * self.x - i * other.x, (i + 1) * self.y - i * other.y)
            if p.in_bounds():
                res.add(p)
            else:
                break
            i += 1

        i = 0
        while True:
            p = Pos((i + 1) * other.x - i * self.x, (i + 1) * other.y - i * self.y)
            if p.in_bounds():
                res.add(p)
            else:
                break
            i += 1
        return res


def get_input(test: bool):
    antennas = defaultdict(list)
    filename = 'inputs/08_test.txt' if test else 'inputs/08.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        dimensions = (len(input_[0]) - 1, len(input_))
        for y, line in enumerate(input_):
            for x, char in enumerate(line[:-1]):
                if char != '.':
                    antennas[char].append(Pos(x, y))
    return antennas, dimensions


def main(test: bool):
    antennas, dimensions = get_input(test)
    Pos.dimensions = dimensions

    part1 = set()
    part2 = set()

    for antenna, positions in antennas.items():
        for i, p1 in enumerate(positions):
            for p2 in positions[i + 1:]:
                ap1, ap2 = p1.get_antinodes_1(p2)
                if ap1.in_bounds():
                    part1.add(ap1)
                if ap2.in_bounds():
                    part1.add(ap2)

                part2 |= p1.get_antinodes_2(p2)

    print('part1:', len(part1))
    print('part2:', len(part2))


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
