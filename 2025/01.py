#!/usr/bin/env python
import time


def get_input(test):
    data = []
    filename = 'inputs/01_test.txt' if test else 'inputs/01.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append((line[:-1]))
    return data


def main(test):
    data = get_input(test)

    sum1 = 0
    sum2 = 0

    position = 50
    for row in data:

        sign = 1 if row[0] == 'R' else -1
        number = sign * int(row[1:])

        if sign == -1 and position == 0:
            pass
            sum2 -= 1

        position += number
        if position % 100 == 0:
            if position > 0:
                sum2 += position // 100
            else:
                sum2 -= position // 100 - 1
        elif position <= 0:
            sum2 -= position // 100
        elif position >= 100:
            sum2 += position // 100

        position %= 100

        if position == 0:
            sum1 += 1

    print('part1:', sum1)
    print('part2:', sum2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
