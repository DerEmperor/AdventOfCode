import time
from scanf import scanf


def main():
    steps = 40
    with open('inputs/14_input.txt', 'r') as file:
        input_ = file.readlines()

    # process input
    rules = dict()
    polymer = dict()

    for i in range(len(input_[0]) - 2):
        pair = input_[0][i:i + 2]
        if pair not in polymer:
            polymer[pair] = 0
        polymer[pair] += 1

    for line in input_[2:]:
        rule = scanf("%s -> %c\n", line)
        rules[rule[0]] = rule[1]

    for step in range(1, steps + 1):
        for pair, number in polymer.copy().items():
            a = pair[0]
            b = rules[pair]
            c = pair[1]
            d = "{}{}".format(a, b)
            e = "{}{}".format(b, c)
            polymer[pair] -= number
            if d not in polymer:
                polymer[d] = 0
            polymer[d] += number
            if e not in polymer:
                polymer[e] = 0
            polymer[e] += number

    chars = dict()
    for pair, number in polymer.items():
        a = pair[0]
        if a not in chars:
            chars[a] = 0
        chars[a] += number
    chars[input_[0][-2]] += 1

    print(max(chars.values()) - min(chars.values()))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
