import time
import re

test_inputs = [
    'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
    'bvwbjplbgvbhsrlpgdmjqwftvncz',
    'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
]


def get_input(test):
    filename = 'inputs/06_test.txt' if test else 'inputs/06.txt'
    with open(filename, 'r') as file:
        input_ = file.readlines()
    return input_[0]


def main(test):
    data = get_input(test)
    #data = test_inputs[4]
    for l in (4, 14):
        for i in range(len(data) - l):
            if len(set(data[i:i + l])) == l:
                print(i + l)
                break


if __name__ == '__main__':
    startTime = time.time()

    print('Test')
    main(True)
    print('real')
    main(False)

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
