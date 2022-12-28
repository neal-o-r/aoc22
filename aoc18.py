def sides(cube):
    x, y, z = cube
    s = {
        (x, y, z + 1),
        (x, y, z - 1),
        (x, y + 1, z),
        (x, y - 1, z),
        (x + 1, y, z),
        (x - 1, y, z),
    }

    return s


if __name__ == "__main__":
    data = open("18.txt").read().split("\n")[:-1]
    cubes = {tuple(map(int, a.split(","))) for a in data}

    print(sum((s not in cubes) for c in cubes for s in sides(c)))

    visited = set()
    frontier = [(0, 0, 0)]

    while frontier:
        curr = frontier.pop()
        # check all adjacent cubes that aren't i) occuppied, ii) visited or iii) outside bounds
        frontier += [
            s for s in (sides(curr) - cubes - visited) if all(-1 <= c <= 20 for c in s)
        ]
        visited.add(curr)

    print(sum((s in visited) for c in cubes for s in sides(c)))
