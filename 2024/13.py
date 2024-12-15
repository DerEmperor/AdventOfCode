#!/usr/bin/env python
import re
import time
import numpy as np

re_input = re.compile(
    r'Button A: X\+(\d+), Y\+(\d+)\n'
    r'Button B: X\+(\d+), Y\+(\d+)\n'
    r'Prize: X=(\d+), Y=(\d+)\n'
)


def get_input(test: bool):
    data = []
    filename = 'inputs/13_test.txt' if test else 'inputs/13.txt'
    with open(filename, 'r') as file:
        input_ = file.read()
    for match in re_input.finditer(input_):
        data.append([int(x) for x in match.groups()])
    return data


def main(test: bool):
    data = get_input(test)
    part1 = 0
    part2 = 0

    for ax, ay, bx, by, px, py in data:
        for offset in [0, 10000000000000]:
            px += offset
            py += offset

            # print(ax, ay, bx, by, px, py)
            det = ax * by - ay * bx
            assert det != 0
            ba = (px * by - py * bx)
            bb = (py * ax - px * ay)

            if ba % det == 0 and bb % det == 0:
                ba_1 = ba // det
                bb_1 = bb // det
                if offset == 0:
                    assert 0 <= ba_1 <= 100, ba_1
                    assert 0 <= bb_1 <= 100, bb_1
                    part1 += 3 * ba_1 + 1 * bb_1
                else:
                    part2 += 3 * ba_1 + 1 * bb_1

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
