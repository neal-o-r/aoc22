from utils import add, directions


def neighbours(grid, pt):
    neighs = []
    i, j = pt
    nx, ny = len(grid), len(grid[0])
    for _, (x, y) in directions.items():
        bounds = (0 <= (i + x) < nx) and (0 <= (j + y) < ny)
        if bounds:
            height = grid[i + x][j + y] <= grid[i][j] + 1
            if height:
                neighs.append(add((i, j), (x, y)))

    return neighs


def djikstra(grid, start, goal=lambda x, y: grid[x][y] == 27):
    visited = {start: 0}
    frontier = [start]

    while frontier:
        curr = frontier.pop(0)
        if goal(*curr):
            return visited
        for n in neighbours(grid, curr):
            alt = visited[curr] + 1
            if (n not in visited) or (alt < visited[n]):
                visited[n] = visited[curr] + 1
                frontier.append(n)


def parse_input(data):
    to_num = lambda x: ord(x) - ord("a") + 1
    data = data.replace("S", "`").replace("E", "{")
    grid = [list(map(to_num, l)) for l in data.split("\n")[:-1]]
    return grid


if __name__ == "__main__":

    data = open("data/12.txt").read()
    grid = parse_input(data)
    start = (20, 0)
    end = (20, 91)

    v = djikstra(grid, start)
    print(v[end] - 2)  # take away two for the start and end

    starts = [
        (i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 1
    ]

    dist_to_end = lambda s: djikstra(grid, s)

    dists = list(dist_to_end(s) for s in starts)
    print(min(d[end] - 2 for d in dists if d))
