from scanf import scanf
import time
import time


def get_overlapping_hor_or_ver():
    with open("inputs/05_input.txt", "r") as file:
        data = file.readlines()

    coords = []
    size = 0
    for line in data:
        coord = scanf("%d,%d -> %d,%d\n", line)
        if coord[0] == coord[2] or coord[1] == coord[3]:
            coords.append(coord)
            size = max(size, max(coord))
    size += 1
    grid = [x[:] for x in [[0] * size] * size]

    for coord in coords:
        for [x, y] in get_points(coord):
            grid[x][y] += 1

    counter = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[x][y] >= 2:
                counter += 1

    return counter


def get_overlapping():
    with open("inputs/05_input.txt", "r") as file:
        data = file.readlines()

    coords = []
    size = 0
    for line in data:
        coord = scanf("%d,%d -> %d,%d\n", line)
        coords.append(coord)
        size = max(size, max(coord))
    size += 1
    grid = [x[:] for x in [[0] * size] * size]

    for coord in coords:
        for [x, y] in get_points(coord):
            grid[x][y] += 1

    counter = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[x][y] >= 2:
                counter += 1

    return counter


def get_points(vec):
    if vec[0] < vec[2]:
        xs = list(range(vec[0], vec[2] + 1))
    else:
        xs = list(range(vec[0], vec[2] - 1, -1))
    if vec[1] < vec[3]:
        ys = list(range(vec[1], vec[3] + 1))
    else:
        ys = list(range(vec[1], vec[3] - 1, -1))

    if len(xs) == 1:
        xs = xs * len(ys)
    if len(ys) == 1:
        ys = ys * len(xs)

    return list(zip(xs, ys))


def my_print(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[x][y], end="")
        print()


def main():
    res = get_overlapping_hor_or_ver()
    print(res)

    res = get_overlapping()
    print(res)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + " ms")
