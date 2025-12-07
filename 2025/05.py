#!/usr/bin/env python
import time
from typing import List, Tuple


def get_input(test: bool) -> Tuple[List[range], List[int]]:
    ranges = []
    numbers = []
    filename = 'inputs/05_test.txt' if test else 'inputs/05.txt'
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                break
            a, b = line[:-1].split('-')
            ranges.append(range(int(a), int(b) + 1))

        for line in file:
            numbers.append(int(line[:-1]))
    return ranges, numbers


def main(test: bool):
    ranges, numbers = get_input(test)

    sum1 = 0

    for n in numbers:
        for r in ranges:
            if n in r:
                sum1 += 1
                break

    merged_ranges: List[range] = [ranges[0]]  # sorted
    for range_in in ranges[1:]:
        idx = 0
        while idx < len(merged_ranges) and merged_ranges[idx].start < range_in.start:
            idx += 1

        merged_ranges.insert(idx, range_in)

        # merge with range before, if necessary
        if idx > 0:
            if merged_ranges[idx].start <= merged_ranges[idx - 1].stop:
                stop = max(merged_ranges[idx].stop, merged_ranges[idx - 1].stop)
                merged_ranges[idx - 1] = range(merged_ranges[idx - 1].start, stop)
                del merged_ranges[idx]
                idx -= 1

        # merge with range after, if necessary
        todo = True
        while todo and idx < len(merged_ranges) - 1:
            todo = False
            if merged_ranges[idx + 1].start <= merged_ranges[idx].stop:
                stop = max(merged_ranges[idx].stop, merged_ranges[idx + 1].stop)
                merged_ranges[idx] = range(merged_ranges[idx].start, stop)
                del merged_ranges[idx + 1]
                todo = True

    sum2 = sum(len(r) for r in merged_ranges)

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
