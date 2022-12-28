from utils import read_file

score_map = {"X": 1, "Y": 2, "Z": 3}


def trans(x):
    return chr(ord(x) + 23) if x < "D" else chr(ord(x) - 23)


def result(elf, you):
    if elf == trans(you):
        # draw
        return 3
    # all ways elf can win
    if (
        (elf == "A" and trans(you) == "C")
        or (elf == "B" and trans(you) == "A")
        or (elf == "C" and trans(you) == "B")
    ):
        return 0
    # you win
    return 6


def score(row):
    elf, you = row.split()
    return score_map[you] + result(elf, you)


def choose(row):
    elf, you = row.split()
    if you == "Y":
        return f"{elf} {trans(elf)}"

    outcome = 6 if you == "Z" else 0

    c = [y for y in "XYZ" if result(elf, y) == outcome][0]

    return f"{elf} {c}"


if __name__ == "__main__":

    data = read_file("data/02.txt")[:-1]
    print(sum(map(score, data)))
    print(sum(map(lambda x: score(choose(x)), data)))
