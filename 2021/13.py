import time
from scanf import scanf
import numpy as np


def main():
    with open('inputs/13_input.txt', 'r') as file:
        input_ = file.readlines()

    # process input
    points = set()
    folding_instructions = []
    i = 0
    while input_[i] != '\n':
        point = scanf("%d,%d\n", input_[i])
        points.add(point)
        i += 1
    i += 1
    for line in input_[i:]:
        instruction = scanf("fold along %c=%d\n", line)
        folding_instructions.append(instruction)
        i += 1
    i = 0
    for (axis, value) in folding_instructions:
        if axis == 'x':
            idx = 0
        elif axis == 'y':
            idx = 1
        else:
            print('ERROR')
            return
        for point in points.copy():
            if point[idx] > value:
                points.remove(point)
                new_value = point[idx] - 2 * (point[idx] - value)
                if axis == 'x':
                    points.add((new_value, point[1]))
                else:
                    points.add((point[0], new_value))
        i += 1
        if i == 1:
            print(len(points))

    shape = (max([p[0] for p in points]) + 1, max([p[1] for p in points]) + 1)

    sheet = np.full(shape, '  ')
    for (x, y) in points:
        sheet[x, y] = '██'

    for line in sheet.transpose():
        print(''.join(line))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
