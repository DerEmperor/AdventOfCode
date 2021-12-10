import time


def get_fuel_linear():
    with open("7_input.txt", "r") as file:
        data = file.readlines()

    crabs = []
    for i in data[0].split(','):
        crabs.append(int(i))

    mini = crabs[0]
    maxi = crabs[0]
    for crab in crabs:
        mini = min(mini, crab)
        maxi = max(maxi, crab)

    min_fuel = (float('inf'))
    for pos in range(mini, maxi + 1):
        fuel = 0
        for crab in crabs:
            fuel += abs(crab - pos)
        if fuel < min_fuel:
            min_fuel = fuel
            min_pos = pos

    return [min_fuel, min_pos]


def get_fuel_quadratic():
    with open("7_input.txt", "r") as file:
        data = file.readlines()

    crabs = []
    for i in data[0].split(','):
        crabs.append(int(i))

    mini = crabs[0]
    maxi = crabs[0]
    for crab in crabs:
        mini = min(mini, crab)
        maxi = max(maxi, crab)

    min_fuel = (float('inf'))
    for pos in range(mini, maxi + 1):
        fuel = 0
        for crab in crabs:
            dif = abs(crab - pos)
            fuel += dif * (dif + 1) // 2
        if fuel < min_fuel:
            min_fuel = fuel
            min_pos = pos

    return [min_fuel, min_pos]


def main():
    res = get_fuel_linear()
    print("{}, {}".format(res[0], res[1]))

    res = get_fuel_quadratic()
    print("{}, {}".format(res[0], res[1]))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + " ms")
