import numpy as np
from scanf import scanf
from sortedcontainers import SortedKeyList


class Node:
    def __init__(self, risk, value=-1, visited=False, previous=None):
        self.risk = risk
        self.value = value
        self.visited = visited
        self.previous = previous

    def __str__(self):
        return "r: {}, v: {}, v: {}".format(self.risk, self.value, self.visited)


def main():
    a = Node(1)
    b = Node(2)
    c = Node(3)
    todo = SortedKeyList([], lambda z: z.risk)
    for e in [b, c, a]:
        print([str(x) for x in todo])
        todo.add(e)

    print([str(x) for x in todo])


if __name__ == '__main__':
    main()
