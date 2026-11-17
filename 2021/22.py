from __future__ import annotations

from typing import List, Tuple, Dict
from collections import defaultdict
import time
import re
import sys

t_cube = tuple[int, int, int, int, int, int]

def part1(instructions) -> int:
    """naive solution"""
    on_cubes = defaultdict(lambda: defaultdict(set))
    for instruction in instructions:
        action, x0, x1, y0, y1, z0, z1 = instruction
        for x in range(x0, x1 + 1):
            if x < -50 or x > 50:
                continue
            for y in range(y0, y1 + 1):
                if y < -50 or y > 50:
                    continue
                for z in range(z0, z1 + 1):
                    if z < -50 or z > 50:
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


def subtract(c2: t_cube, c1: t_cube) -> set[t_cube] | None:
    """Split c2 into multiple cubes by removing c1 (c2 minus c1).

    Returns None if c2 and c1 do not overlap at all, otherwise the set of
    (up to six) disjoint cuboids that make up c2 without c1. All ranges are
    inclusive. This assumes nothing about c1/c2 being related; callers keep
    the stored cubes pairwise disjoint.
    """
    x0, x1, y0, y1, z0, z1 = c2
    a0, a1, b0, b1, e0, e1 = c1

    # intersection of c2 and c1 (inclusive); empty if any axis is empty
    ix0, ix1 = max(x0, a0), min(x1, a1)
    iy0, iy1 = max(y0, b0), min(y1, b1)
    iz0, iz1 = max(z0, e0), min(z1, e1)
    if ix0 > ix1 or iy0 > iy1 or iz0 > iz1:
        return None

    res: set[t_cube] = set()

    def add(px0, px1, py0, py1, pz0, pz1):
        if px0 <= px1 and py0 <= py1 and pz0 <= pz1:
            res.add((px0, px1, py0, py1, pz0, pz1))

    # slabs left/right of the intersection in x, full extent in y and z
    add(x0, ix0 - 1, y0, y1, z0, z1)
    add(ix1 + 1, x1, y0, y1, z0, z1)
    # middle-x, slabs below/above the intersection in y, full extent in z
    add(ix0, ix1, y0, iy0 - 1, z0, z1)
    add(ix0, ix1, iy1 + 1, y1, z0, z1)
    # middle-x, middle-y, slabs below/above the intersection in z
    add(ix0, ix1, iy0, iy1, z0, iz0 - 1)
    add(ix0, ix1, iy0, iy1, iz1 + 1, z1)

    return res


def part2(instructions) -> int:
    # Invariant: `cubes` holds pairwise-disjoint cuboids whose union is
    # exactly the set of cubes currently "on".
    cubes: set[t_cube] = set()
    for instruction in instructions:
        action, x0, x1, y0, y1, z0, z1 = instruction
        new = (x0, x1, y0, y1, z0, z1)

        # Remove the new cuboid from every existing cube it overlaps.
        for old in cubes.copy():
            pieces = subtract(old, new)
            if pieces is not None:
                cubes.discard(old)
                cubes |= pieces

        # Turning on adds the new cuboid itself (turning off just carves it
        # out, which we already did above).
        if action == 'on':
            cubes.add(new)

    return sum(
        (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
        for x0, x1, y0, y1, z0, z1 in cubes
    )


def main():
    filenames = [
        ('small Test', 'inputs/22_input_test.txt', 39, 39),
        ('big Test', 'inputs/22_input_test2.txt', 590784, None),
        ('very big Test', 'inputs/22_input_test3.txt', 474140, 2758514936282235),
        ('real', 'inputs/22_input.txt', 561032, None),
    ]
    regex = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')
    for msg, filename, solution0, solution1 in filenames:
        print(msg)
        with open(filename, 'r') as file:
            input_ = file.readlines()

        instructions = []
        for line in input_:
            instruction = regex.match(line).groups()
            instruction = (instruction[0], *[int(i) for i in instruction[1:]])
            instructions.append(instruction)

        #print('\tpart1: exp:', solution0, 'act:', part1(instructions))
        print('\tpart2: exp:', solution1, 'act:', part2(instructions))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
