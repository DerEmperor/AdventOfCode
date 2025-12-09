#!/usr/bin/env python
import math
import time
from typing import List, Tuple, Set

Coordinate = Tuple[int, int, int]


def get_input(test: bool) -> List[Coordinate]:
    data = []
    filename = 'inputs/08_test.txt' if test else 'inputs/08.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(tuple(int(n) for n in line[:-1].split(',')))
    return data


def main(test: bool):
    nodes = get_input(test)
    edges = []

    for i, c1 in enumerate(nodes):
        x1, y1, z1 = c1
        for c2 in nodes[i + 1:]:
            x2, y2, z2 = c2
            dis = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            edges.append(((x1, y1, z1), (x2, y2, z2), dis))

    sum1 = 0
    sum2 = 0

    nodes = set(nodes)

    edges.sort(key=lambda edge: edge[2])
    circuits: List[Set[Coordinate]] = []
    for step, (c1, c2, dis) in enumerate(edges):

        if step == (10 if test else 1000):
            circuits.sort(key=lambda c: len(c), reverse=True)
            sum1 = len(circuits[0]) * len(circuits[1]) * len(circuits[2])

        added = None
        for circuit in circuits:
            if c1 in circuit:
                if added is None:
                    circuit.add(c2)
                    added = circuit
                else:
                    # merge 2 circuits
                    added.update(circuit)
                    circuits.remove(circuit)
                    break
            elif c2 in circuit:
                if added is None:
                    circuit.add(c1)
                    added = circuit
                else:
                    # merge 2 circuits
                    added.update(circuit)
                    circuits.remove(circuit)
                    break
        if added is None:
            circuits.append({c1, c2})

        nodes -= {c1, c2}

        if len(nodes) == 0:
            # stop
            sum2 = c1[0] * c2[0]
            break

    print('part1:', sum1)
    print('part2:', sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)

    if executionTime < 60:
        print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
    else:
        print(f'Execution time: {round(executionTime, 3)} s')
