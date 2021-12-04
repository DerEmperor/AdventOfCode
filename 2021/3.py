def get_power_consumption():
    with open("3_input.txt", "r") as file:
        data = file.readlines()

    for i in range(len(data)):
        data[i] = data[i][:-1]

    ones = [0] * len(data[0])
    zeros = [0] * len(data[0])

    for string in data:
        for i in range(len(string)):
            if string[i] == '1':
                ones[i] += 1
            else:
                zeros[i] += 1

    gamma = [""] * len(data[0])
    epsilon = [""] * len(data[0])
    for i in range(len(ones)):
        if ones[i] > zeros[i]:
            gamma[i] = "1"
            epsilon[i] = "0"
        else:
            gamma[i] = "0"
            epsilon[i] = "1"

    return [int("".join(epsilon), 2), int("".join(gamma), 2)]


def get_life_support_rating():
    with open("3_input.txt", "r") as file:
        data = file.readlines()

    for i in range(len(data)):
        data[i] = data[i][:-1]

    return 0

def main():
    res = get_power_consumption()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))

    res = get_life_support_rating()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))


if __name__ == '__main__':
    main()
