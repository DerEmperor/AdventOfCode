import time

from scanf import scanf


def add(a, b):
    return '(' + a + ',' + b + ')'


def reduce(number):
    action_done = True
    while action_done:
        action_done = False

        # check number for explosion
        cnt = 0
        for i in range(len(number)):
            c = number[i]
            if c == '(':
                cnt += 1
            elif c == ')':
                cnt -= 1

            if cnt >= 5:
                # explode
                left = number[i + 1]
                right = number[i + 3]
                number = number[:i] + '0' + number[i + 5:]

                # search left
                for j in range(i - 1, -1, -1):
                    if number[j] not in ['(', ')', ',']:
                        number = number[:j] + chr(ord(number[j]) + ord(left) - ord('0')) + number[j + 1:]
                        break

                # search right
                for j in range(i + 2, len(number)):
                    if number[j] not in ['(', ')', ',']:
                        number = number[:j] + chr(ord(number[j]) + ord(right) - ord('0')) + number[j + 1:]
                        break

                action_done = True
                break

        # check for explosion again
        if action_done:
            continue

        # check for split
        for i in range(len(number)):
            c = number[i]
            if c in ['(', ')', ',']:
                continue
            c_num = ord(c) - ord('0')

            if c_num > 9:
                # create pair
                left = chr(ord('0') + c_num // 2)
                right = chr(ord('0') + c_num // 2 + c_num % 2)
                pair = '(' + left + ',' + right + ')'

                # insert pair
                number = number[:i] + pair + number[i + 1:]

                action_done = True
                break

    return number


def get_magnitude(number):
    if number[1] == '(':
        # (pair,unknown)
        # get pair
        cnt = 0
        for end in range(1, len(number)):
            if number[end] == '(':
                cnt += 1
            elif number[end] == ')':
                cnt -= 1

            if cnt == 0:
                break

        a = get_magnitude(number[1:end + 1])
        b = number[end + 2:-1]
        if b[0] == '(':
            # (pair,pair)
            return 3 * a + 2 * get_magnitude(b)
        else:
            # (pair,num)
            return 3 * a + 2 * int(b)

    else:
        # (num,unknown)
        a, b = scanf("(%d,%s)", number)
        if b[0] == '(':
            # (num,pair)
            return 3 * a + 2 * get_magnitude(b)
        else:
            # (num,num)
            return 3 * a + 2 * int(b)


def main():
    with open('inputs/18_input.txt', 'r') as file:
        input_ = file.readlines()
    numbers = [x[:-1].replace('[', '(').replace(']', ')') for x in input_]

    result = numbers[0]

    for number in numbers[1:]:
        result = add(result, number)

        result = reduce(result)

    print(get_magnitude(result))

    max_magnitude = 0
    for number1 in numbers:
        for number2 in numbers:
            if number1 == number2:
                continue
            max_magnitude = max(max_magnitude, get_magnitude(reduce(add(number1, number2))))
    print(max_magnitude)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
