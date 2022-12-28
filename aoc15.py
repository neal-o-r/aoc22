import re
from utils import read_file


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse_line(line):
    num = r"(-?\d+)"
    regex = f"Sensor at x={num}, y={num}: closest beacon is at x={num}, y={num}"
    sx, sy, bx, by = re.findall(regex, line)[0]
    return (int(sx), int(sy)), (int(bx), int(by))


def sensor_beacon_pairs(data):
    return [parse_line(line) for line in data]


def project_to_yaxis(sensor, beacon, yaxis):
    sx, sy = sensor
    d = dist(sensor, beacon)
    d_to_axis = abs(sy - yaxis)

    # if the beacon is closer to the sensor than the yaxis
    # (at the closest point),
    # then the sensor cannot overlap with that yaxis
    # otherwise the sensor can "see" all the pts from xlo to xhi
    x_lo = sx - (d - d_to_axis)
    x_hi = sx + (d - d_to_axis)
    pts_covered = [(x, yaxis) for x in range(x_lo, x_hi + 1)]
    return pts_covered


def covered_pts_on_yaxis(pairs, yaxis):
    pts = set()
    for s, b in pairs:
        pts.update(project_to_yaxis(s, b, yaxis))

    return pts


"""
For part 2:
the uncovered point is unique, so it must be 1 square outside
of the area covered by a sensor (if it was 2 outside, then it wouldn't
be unique). That means if I just generate all of the points one outside
each sensor there should be only one point that isn't covered by a sensor
- by which I mean, it must be further from each sensor than its beacon
"""


def is_answer(x, y, pairs):
    b = 4_000_000
    return (
        x in range(b + 1)
        and y in range(b + 1)
        and all(dist(s, (x, y)) > dist(s, b) for s, b in pairs)
    )


def outside(sensor, beacon):
    d = dist(sensor, beacon)
    r = d + 1
    sx, sy = sensor

    pts = []
    for y in range(sy - r, sy + r + 1):
        d_to_axis = abs(sy - y)
        x_lo = sx - (r - d_to_axis)
        x_hi = sx + (r - d_to_axis)
        pts.append((x_lo, y))
        pts.append((x_hi, y))

    return pts


if __name__ == "__main__":
    data = read_file("data/15.txt")[:-1]
    pairs = sensor_beacon_pairs(data)

    # both parts a and b take AGES to run
    cov = covered_pts_on_yaxis(pairs, 2_000_000)
    # remove from cov any point that already has a beacon on it
    cov = [c for c in cov if c not in list(zip(*pairs))[1]]
    print(len(cov))
    all_candidates = []
    for s, b in pairs:
        all_candidates.extend(outside(s, b))

    get_answer = lambda x: is_answer(*x, pairs)
    a = next(filter(get_answer, all_candidates))

    print(a[0] * 4_000_000 + a[1])
