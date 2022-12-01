from __future__ import annotations

from typing import List, Tuple, Dict
from collections import defaultdict
import time
import re
import sys


def init(instructions, clamp: bool):
    on_cubes = defaultdict(lambda: defaultdict(set))
    for instruction in instructions:
        action, x0, x1, y0, y1, z0, z1 = instruction
        for x in range(x0, x1 + 1):
            if clamp and (x < -50 or x > 50):
                continue
            for y in range(y0, y1 + 1):
                if clamp and (y < -50 or y > 50):
                    continue
                for z in range(z0, z1 + 1):
                    if clamp and (z < -50 or z > 50):
                        continue
                    if action == 'on':
                        on_cubes[x][y].add(z)
                    else:
                        on_cubes[x][y].discard(z)

    cnt = 0
    for ys in on_cubes.values():
        for zs in ys.values():
            cnt += len(zs)
    return cnt


def main():
    filenames = [
        #('small Test', 'inputs/22_input_test.txt', 39, 39),
        #('big Test', 'inputs/22_input_test2.txt', 590784, None),
        ('very big Test', 'inputs/22_input_test2.txt', 474140, 2758514936282235),
        #('real', 'inputs/22_input.txt', None),
    ]
    clamps = [
        True,
        False,
    ]
    regex = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')
    for clamp in clamps:
        for msg, filename, solution0, solution1 in filenames:
            print(msg)
            print('    expected solution:', solution0 if clamp else solution1)
            with open(filename, 'r') as file:
                input_ = file.readlines()

            instructions = []
            for line in input_:
                instruction = regex.match(line).groups()
                instruction = (instruction[0], *[int(i) for i in instruction[1:]])
                instructions.append(instruction)

            print('          my solution:', init(instructions, clamp))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
