from utils import read_file
from collections import defaultdict
from itertools import product
import re


def parse_line(line):
    regex = (
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)"
    )
    loc, rate, others = re.findall(regex, line)[0]
    return loc, int(rate), others.split(", ")


def create_graph(pipes):
    #  create a distance graph
    dist = defaultdict(lambda: 1000)
    for valve, _, neighbours in pipes:
        for n in neighbours:
            dist[valve, n] = 1

    valves = {p[0] for p in pipes}
    for k, i, j in product(valves, valves, valves):  # floyd-warshall
        dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

    return dist, {v: f for v, f, _ in pipes if f > 0}


def dfs(time, curr, available, flows, dists):

    candidates = [a for a in available if dists[curr, a] < time]

    all_flows = [0]
    # this recursive call looks weird since there's no clear base case
    #  but if candidates = [] then we fall through the loop and return 0,
    # and candidates will be 0 if time = 0
    for c in candidates:
        t_ = time - dists[curr, c] - 1
        f = flows[c] * t_
        all_flows.append(f + dfs(t_, c, available - {c}, flows, dists))

    return max(all_flows)


def dfs_elephant(time, curr, available, flows, dists, elephant=False):

    candidates = [a for a in available if dists[curr, a] < time]

    all_flows = [0]
    # check all the candidates for the elephant (or for you if it's a call coming from line 59)
    for c in candidates:
        t_ = time - dists[curr, c] - 1
        f = flows[c] * t_
        all_flows.append(
            f + dfs_elephant(t_, c, available - {c}, flows, dists, elephant=elephant)
        )

    if elephant:
        # for each "level" of the recursion (each set of states)
        # check what the other can do in 26 minutes
        all_flows.append(dfs_elephant(26, "AA", available, flows, dists))

    return max(all_flows)


if __name__ == "__main__":
    data = read_file("test.txt")[:-1]
    pipes = list(map(parse_line, data))

    dists, flows = create_graph(pipes)
    print(dfs(30, "AA", set(flows), flows, dists))
