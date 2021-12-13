import time


def get_power_consumption():
    with open("03_input.txt", "r") as file:
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
    with open("03_input.txt", "r") as file:
        data = file.readlines()

    for i in range(len(data)):
        data[i] = data[i][:-1]

    oxygen_generator_rating = data.copy()
    co2_scrubber_rating = data.copy()

    for i in range(len(data[0])):
        if len(oxygen_generator_rating) == 1 and len(co2_scrubber_rating) == 1:
            break

        if len(oxygen_generator_rating) > 1:
            balance = 0
            for string in oxygen_generator_rating:
                if string[i] == '1':
                    balance += 1
                else:
                    balance -= 1
            if balance >= 0:
                oxygen_bit = '1'
            else:
                oxygen_bit = '0'

        if len(co2_scrubber_rating) > 1:
            balance = 0
            for string in co2_scrubber_rating:
                if string[i] == '1':
                    balance += 1
                else:
                    balance -= 1
            if balance >= 0:
                co2_bit = '0'
            else:
                co2_bit = '1'

            for string in list(oxygen_generator_rating):
                if string[i] != oxygen_bit:
                    oxygen_generator_rating.remove(string)

            for string in list(co2_scrubber_rating):
                if string[i] != co2_bit:
                    co2_scrubber_rating.remove(string)

    return [int("".join(oxygen_generator_rating[0]), 2), int("".join(co2_scrubber_rating[0]), 2)]


def main():
    res = get_power_consumption()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))

    res = get_life_support_rating()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
