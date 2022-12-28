from utils import read_file


def to_list(x):
    return list(map(int, x.split("-")))


def is_contained(a, b):
    a_lo, a_up = to_list(a)
    b_lo, b_up = to_list(b)

    return (a_lo <= b_lo <= b_up <= a_up) or (b_lo <= a_lo <= a_up <= b_up)


def overlaps(a, b):
    a_lo, a_up = to_list(a)
    b_lo, b_up = to_list(b)

    return (a_lo <= b_lo <= a_up) or (b_lo <= a_lo <= b_up)


if __name__ == "__main__":
    data = read_file("./data/04.txt")[:-1]

    do = lambda x: is_contained(*x.split(","))
    print(sum(map(do, data)))

    do = lambda x: overlaps(*x.split(","))
    print(sum(map(do, data)))
