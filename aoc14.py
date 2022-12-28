from utils import read_file, add, sub


def pts_in_range(a, b):
    dx, dy = sub(b, a)

    sx = 1 if dx >= 0 else -1
    sy = 1 if dy >= 0 else -1

    pts = {
        add(a, (sx * x, sy * y))
        for x in range(0, abs(dx) + 1)
        for y in range(0, abs(dy) + 1)
    }

    return pts


def blocked_cells(line):
    pts = [tuple(map(int, p.split(","))) for p in line.split(" -> ")]
    pairs = zip(pts, pts[1:])

    blocked = set()
    for p in pairs:
        blocked.update(pts_in_range(*p))
    return blocked


def fall_to(blocks, start, inf):
    # drop sand until it hits inf (either inf (a) or floor (b))
    curr = start

    free = lambda x: x not in blocks
    while curr[1] < inf:
        possible = [add(curr, s) for s in [(0, 1), (-1, 1), (1, 1)]]
        if all(not free(p) for p in possible):
            return curr

        curr = next(filter(free, possible))

    return curr


def drop_sand_until(blocks, start, inf, cond):
    # drop sand until it hits inf or floor,
    # and return a count of how long it takes
    # until cond is True
    n = 0
    while True:
        sand = fall_to(blocks, start, inf)
        if cond(sand):
            return n

        n += 1
        blocks.add(sand)


def get_blocks(lines):
    blocks = set()
    for l in lines:
        blocks.update(blocked_cells(l))
    return blocks


if __name__ == "__main__":
    lines = read_file("data/14.txt")[:-1]

    blocks = get_blocks(lines)
    inf = max(b[1] for b in blocks) + 1
    cond = lambda x: x[1] == inf
    print(drop_sand_until(blocks, (500, 0), inf, cond))

    blocks = get_blocks(lines)
    floor = max(b[1] for b in blocks) + 1
    cond = lambda x: x == (500, 0)
    print(drop_sand_until(blocks, (500, 0), floor, cond))
