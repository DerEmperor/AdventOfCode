import time
import numpy as np
from sortedcontainers import SortedKeyList


class Node:
    def __init__(self, position, risk, value=-1, visited=False, previous=None):
        self.position = position
        self.risk = risk
        self.value = value
        self.visited = visited
        self.previous = previous

    def __str__(self):
        return "{}, r: {}, v: {}, v: {}".format(self.position, self.risk, self.value, self.visited)


def main():
    with open('15_input.txt', 'r') as file:
        input_ = file.readlines()

    # process input
    small_cave = []
    for x in range(len(input_)):
        small_cave.append([])
        for y in range(len(input_[x]) - 1):
            r = int(input_[x][y])
            node = Node((x, y), r)
            small_cave[x].append(node)
    small_shape = (len(small_cave), len(small_cave[0]))
    shape = (small_shape[0] * 5, small_shape[1] * 5)
    cave = np.zeros(shape).tolist()

    for x in range(shape[0]):
        for y in range(shape[1]):
            node = small_cave[x % small_shape[0]][y % small_shape[1]]

            increase = x // small_shape[0] + y // small_shape[1]
            new_risk = node.risk + increase
            while new_risk > 9:
                new_risk -= 9

            cave[x][y] = Node((x, y), new_risk)

    shape = (len(cave), len(cave[0]))

    todo = SortedKeyList([], lambda a: a.value)

    # first node
    start = cave[0][0]
    start.value = 0

    todo.add(start)

    while len(todo) > 0:
        node = todo.pop(0)
        node.visited = True

        # if node == cave[-1][-1]:
        #    break

        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x = node.position[0] + dx
            y = node.position[1] + dy
            if x < 0 or x >= shape[0] or y < 0 or y >= shape[1]:
                continue

            neighbour = cave[x][y]
            if neighbour.visited:
                continue

            new_value = node.value + neighbour.risk

            if neighbour in todo:
                if new_value < neighbour.value:
                    todo.remove(neighbour)
                else:
                    continue

            neighbour.value = new_value
            neighbour.previous = node
            todo.add(neighbour)

    goal = cave[small_shape[0] - 1][small_shape[1] - 1]
    print(goal)

    goal = cave[-1][-1]
    print(goal)


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
