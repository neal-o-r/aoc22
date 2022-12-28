from itertools import cycle
from tqdm import tqdm


shapes = [
    lambda y: ((2, y), (3, y), (4, y), (5, y)),
    lambda y: ((3, y + 2), (2, y + 1), (3, y + 1), (4, y + 1), (3, y)),
    lambda y: ((4, y + 2), (4, y + 1), (2, y), (3, y), (4, y)),
    lambda y: ((2, y + 3), (2, y + 2), (2, y + 1), (2, y)),
    lambda y: ((2, y + 1), (3, y + 1), (2, y), (3, y)),
]


def not_blocked(shape, blocks):
    return all(((x, y) not in blocks) and (0 <= x < 7) for x, y in shape)


def push(j, shape, blocks):
    x_ = 1 if j == ">" else -1
    new_shape = [(x + x_, y) for x, y in shape]
    possible = not_blocked(new_shape, blocks)
    return new_shape if possible else shape


def total_height(blocks):
    return max(blocks, key=lambda b: b[1])[1]


def can_drop(shape, blocks):
    new_shape = [(x, y - 1) for x, y in shape]
    return not_blocked(new_shape, blocks)


def drop(shapes, jets, blocks, n_blocks):
    i = 0
    for _ in range(n_blocks):
        h = total_height(blocks)
        shape = next(shapes)(h + 4)

        falling = True
        while falling:
            # push if possible
            i, j = next(jets)
            shape = push(j, shape, blocks)
            # if it can drop then do, else break
            if can_drop(shape, blocks):
                shape = [(x, y - 1) for x, y in shape]
            else:
                blocks.update(shape)
                falling = False

    return i, blocks


def find_cycle(shapes, jets, blocks, test=20000):
    # run through drop until we find a
    # cycle, defined as the same jet index
    # and top 7 layers of rocks

    cache = {}
    for n in tqdm(range(test)):
        i, blocks = drop(shapes, jets, blocks, 1)
        h = total_height(blocks)
        # are the top 7 rows the same
        top = tuple((x, h - y) for x, y in blocks if h - y < 7)
        if (i, top) in cache:
            n_old, h_old = cache[(i, top)]
            n_cycle = n - n_old  # how long does it take to cycle
            h_cycle = total_height(blocks) - h_old  # how high is the cycle
            return n_cycle, h_cycle, set(top)

        else:
            cache[(i, top)] = (n, h)


if __name__ == "__main__":
    data = open("17.txt").read().strip("\n")
    shapes = cycle(shapes)
    jets = zip(cycle(range(len(data))), cycle(data))

    # add floor
    blocks = set((x, -1) for x in range(8))
    _, blocks = drop(shapes, jets, blocks, 2022)
    print(total_height(blocks) + 1)  # add one for 0-indexing

    # add floor
    blocks = set((x, -1) for x in range(8))
    shapes = cycle(shapes)
    jets = zip(cycle(range(len(data))), cycle(data))

    n_cycle, h_cycle, top = find_cycle(shapes, jets, blocks)

    target = 1_000_000_000_000

    cycle_height = (target // n_cycle) * h_cycle

    still_to_drop = target % n_cycle

    floor = set((x, -1) for x in range(8))
    _, remaining = drop(shapes, jets, top | floor, still_to_drop)
    h_remaining = total_height(remaining)

    print(cycle_height + h_remaining)
