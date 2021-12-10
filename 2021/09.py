import time


def part1():
    with open('9_input.txt', 'r') as file:
        input_ = file.readlines()

    map = []
    for line in input_:
        map.append([int(x) for x in line[:-1]])

    risk = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            # Top
            if y - 1 >= 0 and map[y - 1][x] <= map[y][x]:
                continue
            # Bottom
            if y + 1 < len(map) and map[y + 1][x] <= map[y][x]:
                continue
            # Left
            if x - 1 >= 0 and map[y][x - 1] <= map[y][x]:
                continue
            # Right
            if x + 1 < len(map[y]) and map[y][x + 1] <= map[y][x]:
                continue
            risk += map[y][x] + 1
    return risk


def part2():
    with open('9_input.txt', 'r') as file:
        input_ = file.readlines()

    map = []
    for line in input_:
        map.append([int(x) for x in line[:-1]])

    # get all low points
    low_points = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            # Top
            if y - 1 >= 0 and map[y - 1][x] <= map[y][x]:
                continue
            # Bottom
            if y + 1 < len(map) and map[y + 1][x] <= map[y][x]:
                continue
            # Left
            if x - 1 >= 0 and map[y][x - 1] <= map[y][x]:
                continue
            # Right
            if x + 1 < len(map[y]) and map[y][x + 1] <= map[y][x]:
                continue
            low_points.append([y, x])

    # find basins
    basin_sizes = []
    for low_point in low_points:
        basin_sizes.append(get_basin_size(map, low_point))
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def get_basin_size(map, point):
    [y, x] = point

    if y < 0 or y >= len(map) or x < 0 or x >= len(map[y]):
        return 0

    if map[y][x] == 9:
        return 0

    map[y][x] = 9
    res = 1
    res += get_basin_size(map, [y, x + 1])
    res += get_basin_size(map, [y, x - 1])
    res += get_basin_size(map, [y + 1, x])
    res += get_basin_size(map, [y - 1, x])
    return res


def main():
    res = part1()
    print(res)

    res = part2()
    print(res)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
