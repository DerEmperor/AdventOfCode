import time
import re
import numpy as np


def get_input(test):
    filename = 'inputs/12_test.txt' if test else 'inputs/12.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    data = []
    start = None
    dst = None

    for y, line in enumerate(input_):
        data.append([])
        for x, c in enumerate(line[:-1]):
            if c == 'S':
                start = x, y
                c = 'a'
            elif c == 'E':
                dst = x, y
                c = 'z'
            val = ord(c) - ord('a')
            data[y].append(val)

    assert start is not None
    assert dst is not None
    return data, start, dst


def main(test):
    data, start, dst = get_input(test)
    size = len(data), len(data[0])
    todo = [(dst, 0)]
    visited = set()
    found = False
    while todo:
        pos, steps = todo.pop(0)
        x, y = pos
        if pos == start:
            print('part 1', steps)
            break
        if data[y][x] == 0 and not found:
            print('part 2', steps)
            found = True

        if pos in visited:
            continue

        visited.add(pos)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x = x + dx
            new_y = y + dy
            new_pos = (new_x, new_y)
            if 0 <= new_x < size[1] and 0 <= new_y < size[0] and data[y][x] <= data[new_y][new_x] + 1:
                todo.append((new_pos, steps + 1))


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
