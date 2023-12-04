#!/usr/bin/env python
import time

NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def get_input(test):
    data = []
    filename = 'inputs/01_test_1.txt' if test else 'inputs/01.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test):
    data = get_input(test)
    sum = 0
    for line in data:
        number = ''
        for c in line:
            if c.isdigit():
                number = c
                break
        for c in line[-1::-1]:
            if c.isdigit():
                number = number + c
                break
        sum += int(number)
    print('1:', sum)
    sum = 0
    for line in data:
        number = ''
        for i in range(len(line)):
            sub = line[i:]
            if sub[0].isdigit():
                number = int(sub[0]) * 10
            for string, n in NUMBERS.items():
                if sub.startswith(string):
                    number = 10 * n
                    break
            if number != '':
                break
        for i in range(len(line) - 1, -1, -1):
            sub = line[i::]
            if sub[0].isdigit():
                number += int(sub[0])
                break
            for string, n in NUMBERS.items():
                if sub.startswith(string):
                    number += n
                    break
            if number % 10 != 0:
                break
        sum += number
    print('2:', sum)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
