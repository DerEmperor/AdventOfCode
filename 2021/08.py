import time
from itertools import permutations


def part1(segment_code):
    with open('inputs/08_input.txt', 'r') as file:
        input_ = file.readlines()

    data = []
    for line in input_:
        data.append([x.split() for x in line[:-1].split('|')])

    counter = 0
    for display in data:
        for digit in display[1]:
            if len(digit) in [len(segment_code[i]) for i in [1, 4, 7, 8]]:
                counter += 1

    return counter


def part2(segment_code_perm):
    with open('inputs/08_input.txt', 'r') as file:
        input_ = file.readlines()

    data = []
    for line in input_:
        data.append([x.split() for x in line[:-1].split('|')])

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    result = 0
    for display in data:
        perms = permutations(letters)
        for perm in perms:
            mapping = dict(zip(letters, perm))
            for digit_corrupted in display[0]:
                digit = swap(digit_corrupted, mapping)
                number = get_digit(digit, segment_code_perm)
                if number == -1:
                    break
            if number == -1:
                continue

            numbers = []
            for digit_corrupted in display[1]:
                digit = swap(digit_corrupted, mapping)
                number = get_digit(digit, segment_code_perm)
                if number == -1:
                    break
                numbers.append(number)

            if number != -1:
                number = numbers[0] * 1000 + numbers[1] * 100 + numbers[2] * 10 + numbers[3]
                result += number
                break

    return result


def swap(string, mapping):
    res = ''
    for c in string:
        res = res + mapping[c]
    return res


def get_digit(digit, segment_code_perm):
    for num, perms in segment_code_perm.items():
        if digit in perms:
            return num
    return -1


def main():
    segment_code = {
        0: ['a', 'b', 'c', 'e', 'f', 'g'],
        1: ['c', 'f'],
        2: ['a', 'c', 'd', 'e', 'g'],
        3: ['a', 'c', 'd', 'f', 'g'],
        4: ['b', 'c', 'd', 'f'],
        5: ['a', 'b', 'd', 'f', 'g'],
        6: ['a', 'b', 'd', 'e', 'f', 'g'],
        7: ['a', 'c', 'f'],
        8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        9: ['a', 'b', 'c', 'd', 'f', 'g']
    }

    segment_code_perm = {}
    for digit, code in segment_code.items():
        segment_code_perm[digit] = [''.join(x) for x in permutations(code)]

    res = part1(segment_code)
    print(res)

    res = part2(segment_code_perm)
    print(res)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
