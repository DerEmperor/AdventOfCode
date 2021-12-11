import time
from statistics import median


def main():
    points_part1 = {'(': 3, ')': 3, '[': 57, ']': 57, '{': 1197, '}': 1197, '<': 25137, '>': 25137}
    points_part2 = {'(': 1, ')': 1, '[': 2, ']': 2, '{': 3, '}': 3, '<': 4, '>': 4}
    with open('10_input.txt', 'r') as file:
        input_ = file.readlines()

    data = []
    for line in input_:
        data.append(line[:-1])

    score_corrupted = 0
    j = 0
    while j < len(data):
        c = data[j][0]
        if c not in ['(', '[', '{', '<']:
            if c in [')', ']', '}', '>']:
                score_corrupted += points_part1[c]
            else:
                print("ERROR")
            continue

        i = 0
        while i < len(data[j]) - 1:
            a, b = data[j][i], data[j][i + 1]
            if (a, b) in [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]:
                if i + 2 < len(data[j]):
                    data[j] = data[j][:i] + data[j][i + 2:]
                else:
                    data[j] = data[j][:i]
                i -= 1
            elif b in ['(', '[', '{', '<']:
                i += 1
            elif b in [')', ']', '}', '>']:
                # corrupted
                score_corrupted += points_part1[b]
                data.pop(j)
                j -= 1
                break
            else:
                # illegal sign
                print("ERROR")
        j += 1

    print(score_corrupted)

    scores_completion = []
    for line in data:
        score = 0
        for i in range(len(line) - 1, -1, -1):
            score = score * 5 + points_part2[line[i]]
        scores_completion.append(score)
    print(median(scores_completion))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
