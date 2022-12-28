directions = {"L": (0, -1), "R": (0, 1), "U": (1, 0), "D": (-1, 0)}


def read_file(fname, delim="\n"):
    return open(fname).read().split(delim)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]
