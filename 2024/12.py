#!/usr/bin/env python
import time
from collections import defaultdict
from typing import Set, Tuple, List

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
NEXT_DIRECTION = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
}


def get_input(test: bool):
    data = []
    filename = 'inputs/12_test_3.txt' if test else 'inputs/12.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append('.' + line[:-1] + '.')
    data.append('.' * len(data[0]))
    data.insert(0, '.' * len(data[0]))
    return data


def get_price(
        data: List[str],
        x: int,
        y: int,
        visited: Set[Tuple[int, int]],
) -> Tuple[int, int, int]:
    assert 1 <= x < len(data[0]) - 1 and 1 <= y < len(data) - 1
    if (x, y) in visited:
        return 0, 0, 0

    area = 1
    perimeter = 0
    sides = 0

    # handle current pos
    visited.add((x, y))
    for dx, dy in DIRECTIONS:
        if data[y][x] == '.':
            # oob
            perimeter += 1
        elif data[y + dy][x + dx] != data[y][x]:
            # adjacent to other food
            perimeter += 1

            ndx, ndy = NEXT_DIRECTION[(dx, dy)]
            # check if it is a new side
            if data[y + ndy][x + ndx] != data[y][x]:
                # corner for a
                # x x
                # a x
                sides += 1
            elif data[y + ndy + dy][x + ndx + dx] == data[y][x]:
                # corner for x
                # x x
                # a x
                sides += 1

        else:
            new_area, new_perimeter, new_sides = get_price(data, x + dx, y + dy, visited)
            area += new_area
            perimeter += new_perimeter
            sides += new_sides

    return area, perimeter, sides


def main(test: bool):
    data = get_input(test)

    part1 = 0
    part2 = 0

    visited = set()

    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '.':
                visited.add((x, y))
                continue
            if (x, y) in visited:
                continue

            area, perimeter, sides = get_price(data, x, y, visited)
            #print(c, area, sides, area * sides)
            part1 += area * perimeter
            part2 += area * sides

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
