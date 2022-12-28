directions = {"^": -1, ">": 1j, "<": -1j, "v": 1, "0": 0}


def create_grid(data):
    maze = {
        (x + y * 1j)
        for x, line in enumerate(data)
        for y, sq in enumerate(line)
        if sq in "." + str(directions.keys())
    }
    blizs = [(x + y * 1j, directions[sq])
        for x, line in enumerate(data)
        for y, sq in enumerate(line)
        if sq in str(directions.keys())
    ]
    return maze, blizs


def wrap(pt):
    x, y = pt.real, pt.imag
    if x == 0:
        return complex(h, y)
    if x == (h+1):
        return complex(1, y)
    if y == 0:
        return complex(x, w)
    if y == (w+1):
        return complex(x, 1)
    return pt


def search(maze, blizs, start, goal):
    frontier = [start]
    count = 0
    while frontier:
        count += 1
        blizs = [(wrap(p + d), d) for p, d in blizs]
        blocs = {p for p, _ in blizs}
        curr = {pt + d for pt in frontier for d in directions.values()}
        frontier = []
        for c in curr:
            if c == goal:
                return count, blizs

            if c not in blocs and c in maze:
                frontier += [c]



if __name__ == "__main__":
    data = list(open("data/24.txt"))
    maze, blizs = create_grid(data)
    h, w = len(data) - 2, len(data[0].strip()) - 2

    start = 1j
    end = 26 + 120j

    t1, blizs = search(maze, blizs, start, end)
    print(t1)

    t2, blizs = search(maze, blizs, end, start)
    print(t1 + t2)

    t3, blizs = search(maze, blizs, start, end)
    print(t1 + t2 + t3)
