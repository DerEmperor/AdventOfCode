import time
import re


def get_input(test):
    filename = 'inputs/04_test.txt' if test else 'inputs/04.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    regex = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)\n')
    res = []
    for line in input_:
        match = regex.match(line)
        assert match
        res.append(tuple(map(int, match.groups())))
    return res


def main(test):
    data = get_input(test)
    score = 0
    score2 = 0
    for a, b, c, d in data:
        assert a <= b and c <= d, f'{a}, {b}, {c}, {d}'
        if a <= c <= d <= b or c <= a <= b <= d:
            score += 1
        if b >= c and d >= a:
            score2 += 1

    print(score)
    print(score2)


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
