
def parse_data(data):
    split_block = lambda s: list(map(int, s.split("\n")))
    return [split_block(b) for b in data]


if __name__ == "__main__":
    data = parse_data(open("./data/01.txt").read().split("\n\n")[:-1])

    cals_per_elf = list(map(sum, data))

    print(max(cals_per_elf))

    print(sum(sorted(cals_per_elf)[-3:]))
