from utils import read_file


def get_views(pos, grid):
    x, y = pos

    right = grid[x][y + 1 :]
    left = grid[x][:y][::-1]

    grid_t = list(map(list, zip(*grid)))
    up = grid_t[y][:x][::-1]
    down = grid_t[y][x + 1 :]

    return up, down, left, right


def is_visible(pos, grid):
    x, y = pos
    for v in get_views(pos, grid):
        if max(v) < grid[x][y]:
            return True

    return False


def takeuntil(pred, lst):
    for l in lst:
        yield l
        if pred(l):
            break


def visible_score(pos, grid):
    x, y = pos

    pred = lambda h: h >= grid[x][y]
    score = 1
    for v in get_views(pos, grid):
        nvis = len(list(takeuntil(pred, v)))
        score *= nvis

    return score


def check_interiors(grid):
    bounds = ((1, len(grid[0]) - 1), (1, len(grid) - 1))

    count = 0
    for x in range(*bounds[0]):
        for y in range(*bounds[1]):
            if is_visible((x, y), grid):
                count += 1

    return count


def view_interiors(grid):
    bounds = ((1, len(grid[0]) - 1), (1, len(grid) - 1))

    return [
        visible_score((x, y), grid)
        for x in range(*bounds[0])
        for y in range(*bounds[1])
    ]


if __name__ == "__main__":
    grid = [list(map(int, x)) for x in read_file("data/08.txt")[:-1]]

    print(check_interiors(grid) + len(grid) * 2 + (len(grid) - 2) * 2)

    print(max(view_interiors(grid)))
