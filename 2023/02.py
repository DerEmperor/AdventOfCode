from __future__ import annotations

import time
from collections import defaultdict

CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def get_input(test):
    data = []
    filename = 'inputs/02_test.txt' if test else 'inputs/02.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            game_i, draws = line[:-1].split(': ')
            id = int(game_i[5:])
            draws_rgb = []
            for draw in draws.split('; '):
                r, g, b = 0, 0, 0
                for tmp in draw.split(', '):
                    val, col = tmp.split(' ')
                    if col == 'red':
                        r = int(val)
                    elif col == 'green':
                        g = int(val)
                    elif col == 'blue':
                        b = int(val)
                    else:
                        print('unknown color')
                        exit(-1)
                draws_rgb.append((r, g, b))

            data.append((id, draws_rgb))
    return data


def main(test):
    data = get_input(test)
    sum1 = 0
    sum2 = 0
    for id, draws in data:
        possible = True
        for r, g, b in draws:
            if r > 12 or g > 13 or b > 14:
                possible = False
                break
        if possible:
            sum1 += id
        min_cubes = tuple((max(draw[i] for draw in draws)) for i in range(3))
        sum2 += min_cubes[0] * min_cubes[1] * min_cubes[2]
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
