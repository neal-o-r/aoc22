import re

dirs = {"R": -1j, "L": 1j}


def path_steps(path):
    return re.findall("(\d+|[LR])", path)


def squares(grid):
    return {
        (x + y * 1j): sq
        for x, line in enumerate(grid)
        for y, sq in enumerate(line)
        if sq in (".#")
    }


def wrap(loc, facing, grid):
    x, y = loc.real, loc.imag
    if facing == 1j:
        # right
        return complex(x, min(p.imag for p in grid if p.real == x))
    if facing == -1j:
        # left
        return complex(x, max(p.imag for p in grid if p.real == x))
    if facing == -1:
        # down
        return complex(max(p.real for p in grid if p.imag == y), y)
    if facing == 1:
        # up
        return complex(min(p.real for p in grid if p.imag == y), y)


def wrap3d(loc, facing):
    x, y = loc.real, loc.imag
    x_face = x // 50
    y_face = y // 50
    if facing == 1j:
        # right
        if x_face == 0:
            return complex(149 - x, 99), -1j
        if x_face == 1:
            return complex(49, x + 50), -1
        if x_face == 2:
            return complex(149 - x, 149), -1j
        if x_face == 3:
            return complex(149, x - 100), -1
    if facing == -1j:
        # left
        if x_face == 0:
            return complex(149 - x, 0), 1j
        if x_face == 1:
            return complex(100, x - 50), 1
        if x_face == 2:
            return complex(149 - x, 50), 1j
        if x_face == 3:
            return complex(0, x - 100), 1
    if facing == 1:
        # down
        if y_face == 0:
            return complex(0, y + 100), 1
        if y_face == 1:
            return complex(100 + y, 49), -1j
        if y_face == 2:
            return complex(-50 + y, 99), -1j
    if facing == -1:
        # up
        if y_face == 0:
            return complex(50 + y, 50), 1j
        if y_face == 1:
            return complex(100 + y, 0), 1j
        if y_face == 2:
            return complex(199, y - 100), -1


def take_step(loc, facing, step, grid):
    if step in dirs:
        facing *= dirs[step]
        return loc, facing

    for _ in range(int(step)):
        l = loc + facing
        d = facing
        if l not in grid:
            l, d = wrap3d(l, facing)
        if grid[l] == "#":
            break
        loc, facing = l, d

    return loc, facing


def walk(steps, loc, facing, grid):
    for s in steps:
        loc, facing = take_step(loc, facing, s, grid)

    return loc, facing


if __name__ == "__main__":
    *grid, _, path = open("data/22.txt")
    steps = path_steps(path)
    sqs = squares(grid)

    loc, facing = walk(steps, 50j, 1j, sqs)
    dir_output = {1j: 0, 1: 1, -1j: 2, -1: 3}
    print(1000 * (loc.real + 1) + 4 * (loc.imag + 1) + dir_output[facing])
