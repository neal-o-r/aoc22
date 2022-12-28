from utils import read_file


def split_blocks(data):
    splits = []
    o = []
    for d in data:
        if d == "":
            splits.append(o)
            o = []
        else:
            o.append(int(d))

    return splits


if __name__ == "__main__":
    data = read_file("./data/01.txt")
    cals_per_elf = list(map(sum, split_blocks(data)))

    print(max(cals_per_elf))

    print(sum(sorted(cals_per_elf)[-3:]))
