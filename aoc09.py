from utils import add, sub, directions


def move_tail(h, t):
    dx, dy = sub(h, t)
    sign = lambda x: 1 if x > 0 else -1
    if max(abs(dx), abs(dy)) > 1:
        if dx:
            t = add(t, (sign(dx), 0))
        if dy:
            t = add(t, (0, sign(dy)))

    return t


def move_head(h, t, moves):
    path = {t}
    for m in moves:
        d, n = m.split()
        for _ in range(int(n)):
            h = add(h, directions[d])
            t = move_tail(h, t)
            path.add(t)

    return path


def move_head_n(h, moves, k=10):
    knots = [h] * k
    path = {knots[-1]}
    for m in moves:
        d, n = m.split()
        for _ in range(int(n)):
            knots[0] = add(knots[0], directions[d])
            for i in range(1, k):
                knots[i] = move_tail(knots[i - 1], knots[i])

            path.add(knots[-1])

    return path


if __name__ == "__main__":
    data = open("data/09.txt").read().split("\n")[:-1]
    h = (0, 0)
    t = (0, 0)

    print(len(move_head(h, t, data)))
    print(len(move_head_n(h, data)))
