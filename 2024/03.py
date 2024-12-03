#!/usr/bin/env python
import re
import time

re_mul = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")


def get_input(test):
    filename = 'inputs/03_test_1.txt' if test else 'inputs/03.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return ''.join(input_)


def main(test):
    data = get_input(test)
    part1 = 0
    part2 = 0
    enabled = True
    for match in re_mul.finditer(data):
        if match.group(0) == 'do()':
            enabled = True
        elif match.group(0) == "don't()":
            enabled = False
        else:
            a, b = [int(x) for x in match.groups()]
            part1 += a * b
            if enabled:
                part2 += a * b

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
