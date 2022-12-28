import re
from operator import le, mul
from functools import reduce


def add(x, y):
    return tuple(xi + yi for xi, yi in zip(x, y))


def sub(x, y):
    return tuple(xi - yi for xi, yi in zip(x, y))


def parse_blueprint(line):
    num = "(\d+)"
    regex = f"Blueprint {num}: Each ore robot costs {num} ore. Each clay robot costs {num} ore. Each obsidian robot costs {num} ore and {num} clay. Each geode robot costs {num} ore and {num} obsidian."
    i, ore, clay, obs_o, obs_c, geo_o, geo_ob = list(
        map(int, re.findall(regex, line)[0])
    )
    # what it costs (ore, clay, obs, geo) -> what you get
    blue = [
        i,
        {
            (1, 0, 0, 0): (ore, 0, 0, 0),
            (0, 1, 0, 0): (clay, 0, 0, 0),
            (0, 0, 1, 0): (obs_o, obs_c, 0, 0),
            (0, 0, 0, 1): (geo_o, 0, geo_ob, 0),
            (0, 0, 0, 0): (0, 0, 0, 0),
        },
    ]
    return blue


def dfs(time, frontier, blueprint):

    if time == 0:
        return max(res[-1] for _, res in frontier)

    candidates = []
    for robots, resources in frontier:
        options = [r for r, c in blueprint.items() if all(map(le, c, resources))]
        resources = add(resources, robots)  #  add a resource for each robot
        for o in options:
            res_ = sub(resources, blueprint[o])  # take away the cost for this robot
            rob_ = add(robots, o)  # add the robot to the robots
            candidates.append((rob_, res_))

    next = sorted(candidates, key=lambda f: add(f[0], f[1])[::-1])[-1500:]

    return dfs(time - 1, next, blueprint)


if __name__ == "__main__":
    data = open("data/19.txt").read().split("\n")[:-1]
    blues = list(map(parse_blueprint, data))

    start = [((1, 0, 0, 0), (0, 0, 0, 0))]
    print(sum(i * dfs(24, start, b) for i, b in blues))

    prod = lambda x: reduce(mul, x, 1)
    print(prod(dfs(32, start, b) for _, b in blues[:3]))
