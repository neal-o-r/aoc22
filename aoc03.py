from utils import read_file


def halves(x):
    n = len(x) // 2
    return x[:n], x[n:]


def overlap(*args):
    return list(set.intersection(*list(map(set, args))))[0]


def score(c):
    offset = ord("A") - 26 if c.isupper() else ord("a")
    return ord(c) - offset + 1


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    data = read_file("./data/03.txt")[:-1]

    do = lambda x: score(overlap(*halves(x)))

    print(sum(map(do, data)))

    groups = list(chunks(data, 3))

    do = lambda x: score(overlap(*x))
    print(sum(map(do, groups)))
