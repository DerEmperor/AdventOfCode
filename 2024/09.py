#!/usr/bin/env python
import time
from typing import List


class File:
    def __init__(self, space, id_):
        self.space = space
        self.id = id_

    def __repr__(self):
        return f'<#{self.id}*{self.space}>'


def get_input(test: bool):
    filename = 'inputs/09_test.txt' if test else 'inputs/09.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return [int(x) for x in input_[0][:-1]]


def print_data(data):
    for x in data:
        if isinstance(x, File):
            for _ in range(x.space):
                print(x.id, end='')
        else:
            for _ in range(x):
                print('.', end='')
    print()


def main(test: bool):
    data = get_input(test)
    data_cpy = data[:]

    part1 = 0

    idx = 0
    id_front = 0
    id_back = len(data) // 2
    while data:
        # consume file
        file_size = data.pop(0)
        for _ in range(file_size):
            part1 += idx * id_front
            idx += 1
        id_front += 1

        # consume free space
        if data:
            space_size = data.pop(0)
            while space_size > 0:
                data[-1] -= 1
                space_size -= 1
                part1 += idx * id_back
                idx += 1
                if data[-1] <= 0:
                    data = data[:-2]
                    id_back -= 1

    print('part1:', part1)

    part2 = 0
    data = []
    id_ = 0
    for i, x in enumerate(data_cpy):
        if i % 2 == 0:
            data.append(File(x, id_))
            id_ += 1
        else:
            data.append(x)

    end = len(data) - 1
    while end > 0:
        # print_data(data)
        file = data[end]
        moved = False
        for j in range(end):
            if j % 2 == 0:
                # file
                continue
            else:
                # space
                space = data[j]
                if file.space <= space:
                    # move data
                    data[j] = 0
                    data.insert(j + 1, file)
                    data.insert(j + 2, space - file.space)
                    data.pop(end + 2)
                    data[end + 1] += file.space
                    moved = True
                    break
        if not moved:
            end -= 2

    i = 0
    for x in data:
        if isinstance(x, File):
            for _ in range(x.space):
                part2 += i * x.id
                i += 1
        else:
            i += x

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
