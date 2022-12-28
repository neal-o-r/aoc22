from functools import cmp_to_key


def parse_pair(data):
    l, r = data.split("\n")
    return eval(l), eval(r)


def tway(l, r):
    # do a 3-way comparison
    return 0 if l == r else (1 if l < r else -1)


def compare(left, right):
    types = type(left), type(right)
    if types == (int, int):
        return tway(left, right)
    if types == (int, list):
        return compare([left], right)
    if types == (list, int):
        return compare(left, [right])

    for l, r in zip(left, right):
        c = compare(l, r)
        if c != 0:
            # if there's a definite answer
            return c

    # if there's no definite answer, use length
    return tway(len(left), len(right))


if __name__ == "__main__":

    data = open("data/13.txt").read().split("\n\n")[:-1]
    pairs = list(map(parse_pair, data))

    print(sum(i + 1 for i, p in enumerate(pairs) if compare(*p) == 1))

    flat = sum(map(list, pairs), [])

    markers = [[[2]], [[6]]]
    flat += markers

    flat_sort = sorted(flat, key=cmp_to_key(compare), reverse=True)
    print((flat_sort.index(markers[0]) + 1) * (flat_sort.index(markers[1]) + 1))
