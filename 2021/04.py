import time


def get_winning_score():
    with open("inputs/04_input.txt", "r") as file:
        data = file.readlines()

    numbers = [int(x) for x in data[0].split(",")]
    boards = []

    counter = 0
    for line in data[2:]:
        if counter % 6 == 5:
            counter += 1
            continue
        elif counter % 6 == 0:
            boards.append([])
        boards[counter // 6].extend([int(x) for x in line.split()])
        counter += 1

    for number in numbers:
        for board in boards:
            if number in board:
                board[board.index(number)] = -1
                for i in range(5):
                    if board[i * 5:i * 5 + 5] == [-1] * 5 or board[i:-1:5] == [-1] * 5:
                        # bingo
                        return [sum([x if x != -1 else 0 for x in board]), number]
    return [0, 0]


def get_loosing_score():
    with open("inputs/04_input.txt", "r") as file:
        data = file.readlines()

    numbers = [int(x) for x in data[0].split(",")]
    boards = []

    counter = 0
    for line in data[2:]:
        if counter % 6 == 5:
            counter += 1
            continue
        elif counter % 6 == 0:
            boards.append([])
        boards[counter // 6].extend([int(x) for x in line.split()])
        counter += 1

    for number in numbers:
        for board in list(boards):
            if number in board:
                board[board.index(number)] = -1
                for i in range(5):
                    if board[i * 5:i * 5 + 5] == [-1] * 5 or board[i:-1:5] == [-1] * 5:
                        # bingo
                        boards.remove(board)
                        res = [sum([x if x != -1 else 0 for x in board]), number]
                        break
    return res


def main():
    res = get_winning_score()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))

    res = get_loosing_score()
    print("{} * {} = {}".format(res[0], res[1], res[0] * res[1]))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
