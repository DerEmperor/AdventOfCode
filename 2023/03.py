#!/usr/bin/env python
import time
from collections import defaultdict


def get_input(test):
    data = []
    filename = 'inputs/03_test2.txt' if test else 'inputs/03.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append('.' + line[:-1] + '.')
    data.append(''.join(['.'] * len(data[0])))
    data.insert(0, ''.join(['.'] * len(data[0])))

    return data


def next_to_symbol(data, row, start, end):
    adjacent_symbol = False
    lines = [
        (row - 1, data[row - 1]),  # upper
        (row, data[row]),  # middle
        (row + 1, data[row + 1]),  # lower
    ]

    for row, line in lines:
        for col, c in enumerate(line[start - 1:end + 2], start - 1):
            if (not c.isdigit()) and c != '.':
                adjacent_symbol = True
                if c == '*':
                    return True, row, col

    return (adjacent_symbol,)


def main(test):
    data = get_input(test)
    sum1 = 0
    gears = defaultdict(list)
    for row, line in enumerate(data):
        start = 0
        while start < len(line):
            if line[start] == '6':
                a = 4
            if line[start].isdigit():
                end = start
                while line[end + 1].isdigit():
                    end += 1
                res = next_to_symbol(data, row, start, end)
                if res[0]:
                    number = int(line[start:end + 1])
                    sum1 += number
                    if len(res) > 1:
                        gears[(res[1], res[2])].append(number)

                start = end + 1

            else:
                start += 1

    sum2 = 0
    for (row, col), numbers in gears.items():
        if len(numbers) == 2:
            sum2 += numbers[0] * numbers[1]

    print(sum1)
    print(sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
