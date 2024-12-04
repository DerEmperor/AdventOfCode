#!/usr/bin/env python
import time

'''
+---> x
|
|
v
y
'''

directions = [
    ((0, 1), (0, 2), (0, 3)),  # right
    ((1, 1), (2, 2), (3, 3)),  # down right
    ((1, 0), (2, 0), (3, 0)),  # down
    ((-1, 1), (-2, 2), (-3, 3)),  # down left
    ((0, -1), (0, -2), (0, -3)),  # left
    ((-1, -1), (-2, -2), (-3, -3)),  # up left
    ((-1, 0), (-2, 0), (-3, 0)),  # up
    ((1, -1), (2, -2), (3, -3)),  # up right
]


def get_input(test):
    data = []
    filename = 'inputs/04_test.txt' if test else 'inputs/04.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            data.append(line[:-1])
    return data


def main(test):
    data = get_input(test)

    # pad data
    for i in range(len(data)):
        data[i] = '...' + data[i] + '...'
    for _ in range(3):
        data.insert(0, '.' * len(data[0]))
        data.append('.' * len(data[0]))

    part1 = 0
    part2 = 0

    for y in range(2, len(data) - 3):
        for x in range(2, len(data[0]) - 3):
            for (x1, y1), (x2, y2), (x3, y3) in directions:
                if (
                        data[y][x] == 'X' and
                        data[y + y1][x + x1] == 'M' and
                        data[y + y2][x + x2] == 'A' and
                        data[y + y3][x + x3] == 'S'
                ):
                    part1 += 1

            if (
                    data[y][x] in 'MS' and
                    data[y][x + 2] in 'MS' and
                    data[y + 1][x + 1] == 'A' and
                    data[y + 2][x] in 'MS' and
                    data[y + 2][x + 2] in 'MS' and
                    data[y][x] != data[y + 2][x + 2] and
                    data[y + 2][x] != data[y][x + 2]
            ):
                part2 += 1

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
