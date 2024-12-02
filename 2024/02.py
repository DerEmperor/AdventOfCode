#!/usr/bin/env python
import time
from operator import truediv


def get_input(test):
    data = []
    filename = 'inputs/02_test.txt' if test else 'inputs/02.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append([int(x) for x in line[:-1].split(' ')])
    return data


def is_save(line) -> bool:
    if len(line) < 2:
        return True
    else:
        asc = True
        desc = True
        for a, b in zip(line, line[1:]):
            if a >= b:
                asc = False
            if a <= b:
                desc = False
            if abs(a - b) > 3:
                asc = False
                desc = False
                break
        if asc or desc:
            return True
    return False


def main(test):
    data = get_input(test)
    part1 = 0
    part2 = 0

    for line in data:
        if is_save(line):
            part1 += 1
            part2 += 1
        else:
            for i in range(len(line)):
                removed = line[i]
                del line[i]
                if is_save(line):
                    part2 += 1
                    break
                line.insert(i, removed)


    print('part1:', part1)
    print('part2:', part2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
