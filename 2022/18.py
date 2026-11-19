#!/usr/bin/env python
import os
import sys
import time

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


def get_input(test: bool) -> list[tuple[int, int, int]]:
    data = []
    filename = 'inputs/18_test.txt' if test else 'inputs/18.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(tuple(int(x) for x in line[:-1].split(',')))
    return data


def part1(data: set[tuple[int, int, int]]) -> int:
    res = 0
    for x, y, z in data:
        res += 3
        for dx, dy, dz in [(0, 0, 1), (0, 1, 0), (1, 0, 0)]:
            if (x + dx, y + dy, z + dz) in data:
                res -= 1
            else:
                res += 1
    return res


def part2(data: set[tuple[int, int, int]]) -> int:
    """fill space and count sides"""
    min_x = min(c[0] for c in data) - 1
    max_x = max(c[0] for c in data) + 1
    min_y = min(c[1] for c in data) - 1
    max_y = max(c[1] for c in data) + 1
    min_z = min(c[2] for c in data) - 1
    max_z = max(c[2] for c in data) + 1
    res = 0
    todo = [(min_x, min_y, min_z)]
    visited = {(min_x, min_y, min_z)}
    while todo:
        x, y, z = todo.pop(0)
        for dx, dy, dz in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
            next_point = (x + dx, y + dy, z + dz)
            if next_point in data:
                res += 1
            else:
                if (
                        min_x <= next_point[0] <= max_x and
                        min_y <= next_point[1] <= max_y and
                        min_z <= next_point[2] <= max_z
                ):
                    # in bounds
                    if next_point not in visited:
                        todo.append(next_point)
                        visited.add(next_point)
    return res


def main(test: bool):
    data = get_input(test)

    sum1 = part1(set(data))
    sum2 = part2(set(data))

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [64, 3542]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [58, 2080]:
        raise WrongAnswer('part2')


if __name__ == '__main__':
    startTime = time.time()

    try:
        print('Test')
        main(True)
        print('real')
        sys.stdout = open(os.devnull, 'w')  # suppress test prints
        main(False)

    finally:
        executionTime = (time.time() - startTime)

        if executionTime < 60:
            print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
        else:
            print(f'Execution time: {round(executionTime, 3)} s')
