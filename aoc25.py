
def symbol(s):
    if s.isnumeric():
        return int(s)
    if s == "-":
        return -1
    if s == "=":
        return -2


def snafu_convert(snafu):
    if len(snafu) == 0:
        return 0
    *a, b = snafu
    return 5 * snafu_convert(a) + ("=-012".find(b) - 2)


def num_convert(num):
    if num == 0:
        return ""
    a, b = divmod(num + 2, 5)
    return num_convert(a) + '=-012'[b]


if __name__ == "__main__":
    snafus = open("data/25.txt").read().split("\n")[:-1]
    n = sum(snafu_convert(s) for s in snafus)
    print(num_convert(n))


