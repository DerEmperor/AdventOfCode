import time

import numpy as np


def count_increasing():
    data = np.loadtxt('01_input.txt', dtype='int')

    number = 0

    for i in range(1, len(data)):
        if data[i - 1] < data[i]:
            number += 1

    return number


def count_increasing_three():
    data = np.loadtxt('01_input.txt', dtype='int')

    number = 0

    for i in range(0, len(data) - 3):
        if sum(data[i:i + 3]) < sum(data[i + 1:i + 4]):
            number += 1

    return number


def main():
    res = count_increasing()
    print(res)
    res = count_increasing_three()
    print(res)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
