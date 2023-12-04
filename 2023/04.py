#!/usr/bin/env python
import time

def get_input(test):
    data = []
    filename = 'inputs/04_test.txt' if test else 'inputs/04.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            win, yours = line[:-1].split(': ')[1].split(' | ')
            tmp = (
                [int(n) for n in win.split()],
                [int(n) for n in yours.split()],
            )
            data.append(tmp)

    return data


def main(test):
    data = get_input(test)
    sum1 = 0
    sum2 = 0
    buf = [1] * len(data[0][0])
    for win, yours in data:
        match_cnt = len(set(win) & set(yours))

        sum1 += int(2 ** (match_cnt - 1))

        cards = buf.pop(0)
        buf.append(1)
        sum2 += cards
        for i in range(match_cnt):
            buf[i] += cards



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
