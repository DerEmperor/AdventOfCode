import itertools
import time


def main():
    print(sum(int(''.join('53460_1_7_92__8'
                          [(len(o) * len(o & (l := {len(s): set(s) for s
                                                    in x.split()})[4]) + len(o & l[2])) % 16] for
                          o in map(set, y.split()))) for
              x, y in [x.split('|') for x in open('8_input.txt')]))


if __name__ == '__main__':
    startTime = time.time()

    main()

    executionTime = (time.time() - startTime)
    print('Execution time: ' + str(round(executionTime * 1000, 6)) + ' ms')
