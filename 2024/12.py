#!/usr/bin/env python
import time
from collections import defaultdict
from typing import Set, Tuple, List


def get_input(test: bool):
    data = []
    filename = 'inputs/12_test.txt' if test else 'inputs/12.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def get_price(
        data: List[str],
        x: int,
        y: int,
        visited: Set[Tuple[int, int]],
) -> Tuple[int, int, int]:
    assert 0 <= x < len(data[0]) and 0 <= y < len(data)
    if (x, y) in visited:
        return 0, 0, 0

    area = 1
    perimeter = 0
    sides = 0

    # handle current pos
    visited.add((x, y))
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if not (0 <= x + dx < len(data[0]) and 0 <= y + dy < len(data)):
            # oob
            perimeter += 1
        elif data[y + dy][x + dx] != data[y][x]:
            # adjacent to other food
            perimeter += 1

            # check if it is a new side
            if dy == 0:
                if (
                        (y-1 >= 0 and data[y - 1][x] == data[y][x]) ==
                        (y + 1 < len(data) and
                         0 <= x + dx < len(data[0]) and
                         data[y][x] == data[y + 1][x + dx])
                ):  # xnor
                    sides += 1
            elif dx == 0:
                if (
                        (x + 1 < len(data[0]) and data[y][x + 1] == data[y][x]) ==
                        (
                                0 <= y + dy < len(data[0]) and
                                x + 1 < len(data[0]) and
                                data[y][x] == data[y + dy][x + 1]
                        )
                ):  # xnor
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
            if (x, y) in visited:
                continue

            area, perimeter, sides = get_price(data, x, y, visited)
            print(c, area, sides, area * sides)
            part1 += area * perimeter
            part2 += area * sides

    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    #main(False)

    executionTime = (time.time() - startTime)
    if executionTime > 1:
        print('Execution time:', str(round(executionTime, 1)), 's')
    else:
        print('Execution time:', str(round(executionTime * 1000, 1)), 'ms')
