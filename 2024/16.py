#!/usr/bin/env python
from __future__ import annotations

from collections import defaultdict
from enum import Enum
import time
from heapq import heappush, heapify, heappop
from typing import List, Tuple, Set


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __lt__(self, other):
        return True

    def __repr__(self):
        return self.name


def get_input(test: bool):
    data = []
    filename = 'inputs/16_test_2.txt' if test else 'inputs/16.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test: bool):
    maze = get_input(test)
    end = None

    distances = {}
    pq = []
    prev = defaultdict(set)
    for y, line in enumerate(maze):
        for x, c in enumerate(line):
            if c == 'S':
                for d in Direction:
                    if d == Direction.EAST:
                        pq.append((0, x, y, d))
                        distances[x, y, d] = 0
                    else:
                        distances[x, y, d] = float('inf')
                    distances[x, y, d] = 0
            elif c == '.':
                for d in Direction:
                    distances[x, y, d] = float('inf')
            elif c == 'E':
                end = (x, y)
                for d in Direction:
                    distances[x, y, d] = float('inf')

    heapify(pq)
    min_cost = None
    while pq:
        cost, x, y, d = heappop(pq)
        if maze[y][x] == 'E':
            min_cost = cost
        if min_cost is not None and cost > min_cost:
            break

        for dd in Direction:
            dx, dy = dd.value
            new_cost = cost + 1 if dd == d else cost + 1001  # turn around is always more expensive
            if maze[y + dy][x + dx] != '#' and new_cost <= distances[x + dx, y + dy, dd]:
                if new_cost < distances[x + dx, y + dy, dd]:
                    distances[x + dx, y + dy, dd] = new_cost
                    prev[x + dx, y + dy, dd].clear()
                prev[x + dx, y + dy, dd].add((x, y, d))
                heappush(pq, (new_cost, x + dx, y + dy, dd))

    print('part1:', min_cost)

    tiles = {end}
    todo = [(*end, d) for d in Direction]
    while todo:
        node = todo.pop(0)
        for x, y, d in prev[node]:
            tiles.add((x, y))
            todo.append((x, y, d))
    print('part2:', len(tiles))


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
