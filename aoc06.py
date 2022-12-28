def find_block(pack, n):
    for i in range(n, len(pack) - 1):
        prev = pack[i - n : i]
        if len(set(prev)) == n:
            return i


if __name__ == "__main__":

    with open("data/06.txt") as f:
        data = f.read()

    print(find_block(data, 4))
    print(find_block(data, 14))
