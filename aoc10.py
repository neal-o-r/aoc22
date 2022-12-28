def run(program):
    cycle = 0
    x = 1
    state = [(cycle, x)]
    for p in program:
        cycle += 1
        state.append((cycle, x))
        if p.startswith("addx"):
            _, n = p.split()

            cycle += 1
            state.append((cycle, x))
            x += int(n)

    return state


def draw(states):
    screen = []
    for p, x in states:
        i, j = (p - 1) % 40, (p - 1) // 40
        if i in [x, x + 1, x - 1]:
            screen.append((i, j))

    return screen


if __name__ == "__main__":
    data = open("data/10.txt").read().split("\n")[:-1]

    states = run(data)
    cycles = [20, 60, 100, 140, 180, 220]
    print(sum(states[c][1] * c for c in cycles))

    pixels = draw(states)

    for i in range(6):
        print("")
        for j in range(40):
            if (j, i) in pixels:
                print("#", end="")
            else:
                print(".", end="")
