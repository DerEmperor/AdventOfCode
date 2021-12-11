import time
import numpy as np


def main():
    sync = False
    steps = 100
    with open('11_input.txt', 'r') as file:
        input_ = file.readlines()

    data = []
    for line in input_:
        data.append([int(x) for x in line[:-1]])
    data = np.array(data)

    flashes = 0
    for step in range(1, steps + 1):
        # increase every number by 1
        data[:, :] = data[:, :] + np.ones(data.shape, dtype=int)

        # get flashes
        for x, y in np.ndindex(data.shape):
            if data[x, y] > 9:
                flashes += get_flashes(data, x, y)

        if (not sync) and np.all(data == 0):
            sync = True
            print("step:", step + 1)

    print("flashes:", flashes)

    while not sync:
        # increase every number by 1
        data[:, :] = data[:, :] + np.ones(data.shape, dtype=int)

        # get flashes
        for x, y in np.ndindex(data.shape):
            if data[x, y] > 9:
                flashes += get_flashes(data, x, y)

        if np.all(data == 0):
            sync = True
            print("step:", step + 1)

        step += 1


def get_flashes(data, x, y):
    # out of range
    if (x, y) not in np.ndindex(data.shape):
        return 0

    # already flashed
    if data[x, y] <= 0:
        return 0

    # increase energy
    data[x, y] += 1

    if data[x, y] > 9:
        # dumbo octopuses flashes
        data[x, y] = 0
        flashes = 1
        for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            flashes += get_flashes(data, x + dx, y + dy)

        return flashes
    else:
        return 0


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
