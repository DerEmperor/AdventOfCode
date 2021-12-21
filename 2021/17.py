import sys
import time
import math
from scanf import scanf


def main():
    with open('inputs/17_input.txt', 'r') as file:
        input_ = file.readlines()

    target = scanf("target area: x=%d..%d, y=%d..%d\n", input_[0])

    x_min = min(target[0], target[1])
    x_start = int(0.5 * ((8 * x_min + 1) ** 0.5) - 1)
    x_max = max(target[0], target[1])

    y_min = min(target[2], target[3])
    y_max = max(target[2], target[3])

    max_height = 0
    counter = 0

    for start_x in range(x_start, x_max + 1):
        for start_y in range(-1000, 1000):
            velocity = [start_x, start_y]
            position = [0, 0]
            cur_max_height = 0
            step = 1
            while True:
                last_y = position[1]
                position[0] += velocity[0]
                position[1] += velocity[1]

                cur_max_height = max(cur_max_height, position[1])

                if velocity[0] > 0:
                    velocity[0] -= 1
                velocity[1] -= 1

                if position[0] in range(x_min, x_max + 1) and position[1] in range(y_min, y_max + 1):
                    max_height = max(max_height, cur_max_height)
                    counter += 1
                    break

                if velocity[0] == 0 and position[0] not in range(x_min, x_max + 1):
                    break

                if velocity[0] >= 0 and position[0] > x_max:
                    break

                if y_min > last_y > position[1]:
                    break

                step += 1

    print(max_height)
    print(counter)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 3)) + ' ms')
