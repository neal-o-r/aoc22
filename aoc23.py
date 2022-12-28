directions = {
    "N": (-1, -1 - 1j, -1 + 1j),
    "S": (1, 1 - 1j, 1 + 1j),
    "W": (-1j, -1 - 1j, 1 - 1j),
    "E": (1j, 1 + 1j, -1 + 1j),
}


def create_grid(data):
    return {
        (x + y * 1j)
        for x, line in enumerate(data)
        for y, sq in enumerate(line)
        if sq == "#"
    }


def shift(lst):
    return lst[1:] + [lst[0]]


def test_directions(elf, elves, dirs):
    for d in dirs:
        if all(elf + w not in elves for w in directions[d]):
            return d

    return None


def play_round(elves, dirs):
    moves = []
    for elf in elves:
        m = test_directions(elf, elves, dirs)
        neighbours = sum(
            elf + d in elves for d in set(sum(map(list, directions.values()), []))
        )
        if neighbours == 0:
            moves.append(elf)
        elif m:
            moves.append(elf + directions[m][0])
        else:
            moves.append(elf)

    new_elves = {
        new if moves.count(new) == 1 else elf for elf, new in zip(elves, moves)
    }

    dirs = shift(dirs)
    return new_elves, dirs


def run(elves, dirs, n):
    for _ in range(n):
        elves, dirs = play_round(elves, dirs)

    return elves


def run_convergence(elves, dirs):
    n = 1
    new_elves, dirs = play_round(elves, dirs)
    while new_elves != elves:
        if not n % 100:
            print(n)
        elves = new_elves
        new_elves, dirs = play_round(elves, dirs)
        n += 1

    return n


def bounds(x):
    return int(min(x)), int(max(x))


def empty_sqs(elves):
    x_min, x_max = bounds([x.real for x in elves])
    y_min, y_max = bounds([x.imag for x in elves])
    return (x_max - x_min + 1) * (y_max - y_min + 1) - len(elves)


if __name__ == "__main__":
    data = list(open("data/23.txt"))
    elves = create_grid(data)
    dirs = list(directions.keys())

    elves_end = run(elves, dirs, 10)
    print(empty_sqs(elves_end))
    print(run_convergence(elves, dirs))
