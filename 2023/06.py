#!/usr/bin/env python
import time
from math import ceil, sqrt


def get_input(test):
    data = []
    filename = 'inputs/06_test.txt' if test else 'inputs/06.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        times = input_[0].split(':')[1].split()
        distances = input_[1].split(':')[1].split()

    return times, distances


def get_res(times, distances):
    res = 1
    for t, d in zip(times, distances):
        # my_distance = i * (t - i)
        a = (t - sqrt(t * t - 4 * d)) / 2
        b = (t + sqrt(t * t - 4 * d)) / 2
        wins = int(b - 0.000000000001) - ceil(a + 0.000000000001) + 1  # I know that the offset is dirty
        res *= wins
    return res


def main(test):
    times, distances = get_input(test)

    ts = [int(t) for t in times]
    ds = [int(d) for d in distances]
    part1 = get_res(ts, ds)
    print(part1)

    ts = [int(''.join(times))]
    ds = [int(''.join(distances))]
    part2 = get_res(ts, ds)
    print(part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
