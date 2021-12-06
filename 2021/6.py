import time


def get_number_of_fishes_naive(days):
    with open("6_input.txt", "r") as file:
        data = file.readlines()

    fishes = []
    for i in data[0].split(','):
        fishes.append(int(i))

    for day in range(1, days + 1):
        n = len(fishes)
        for i in range(n):
            fishes[i] -= 1
            if fishes[i] < 0:
                fishes[i] = 6
                fishes.append(8)

    return len(fishes)


def get_number_of_fishes(days):
    with open("6_input.txt", "r") as file:
        data = file.readlines()

    fishes = [0] * 9
    for i in data[0].split(','):
        number = int(i)
        fishes[number] += 1

    for day in range(1, days + 1):
        fishes[7] += fishes[0]
        fishes = [*fishes[1:], fishes[0]]

    return sum(fishes)


def main():
    res = get_number_of_fishes_naive(80)
    print(res)

    res = get_number_of_fishes(256)
    print(res)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + " ms" )
