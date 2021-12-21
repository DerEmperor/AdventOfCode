import time


def get_position():
    f = open('inputs/02_input.txt', "r")
    data = f.readlines()
    f.close()

    depth = 0
    horizontal_position = 0

    for command in data:
        [direction, value] = command.split()
        value = int(value)
        if direction == 'down':
            depth += value
        if direction == 'up':
            depth -= value
        if direction == 'forward':
            horizontal_position += value

    return [depth, horizontal_position]


def get_position_with_aim():
    f = open('inputs/02_input.txt', "r")
    data = f.readlines()
    f.close()

    aim = 0
    depth = 0
    horizontal_position = 0

    for command in data:
        [direction, value] = command.split()
        value = int(value)
        if direction == 'down':
            aim += value
        if direction == 'up':
            aim -= value
        if direction == 'forward':
            horizontal_position += value
            depth += aim * value

    return [depth, horizontal_position]


def main():
    res = get_position()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))

    res = get_position_with_aim()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
