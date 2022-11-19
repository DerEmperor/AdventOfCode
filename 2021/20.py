from __future__ import annotations
from typing import List
import time

runs = 50


def add_frame(data: List[List[str]], char: str) -> List[List[str]]:
    new_data = [[char] * (len(data[0]) + 2)]
    for row in data:
        new_data.append([char, *row, char])
    new_data.append([char] * (len(data[0]) + 2))
    return new_data


def main():
    # read data
    #with open('inputs/20_input_test.txt', 'r') as file:
    with open('inputs/20_input.txt', 'r') as file:
        input_ = file.readlines()
    iea = input_[0][:-1]
    data = []
    for row in input_[2:]:
        data.append([c for c in row[:-1]])

    data = add_frame(data, '.')

    for row in data:
        print(''.join(row))

    # apply algorithm
    for run in range(runs):
        data = add_frame(data, '#' if run % 2 == 1 and iea[0] == '#' else '.')
        new_data = [row[:] for row in data]

        # apply algorithm by creating new matrix
        for i in range(len(data)):
            for j in range(len(data[0])):
                integer_str = []
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        try:
                            char = data[k][l]
                        except IndexError:
                            char = '#' if run % 2 == 1 and iea[0] == '#' else '.'
                        integer_str.append('0' if char == '.' else '1')
                integer = int(''.join(integer_str), 2)
                new_data[i][j] = iea[integer]
        data = new_data

        counter = 0
        for row in data:
            for c in row:
                if c == '#':
                    counter += 1
                print(c, end='')
            print('')
        print('run', run + 1, ':', counter)


if __name__ == '__main__':
    print('solution test: ', 35)
    print('solution: ', 5044)
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
