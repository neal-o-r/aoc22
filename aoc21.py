from utils import read_file
from operator import add, sub, mul, truediv

ops = {"+": add, "-": sub, "*": mul, "/": truediv}


def evaluate(item, root=False):
    if item.isnumeric():
        return int(item)
    elif item == "1j":
        return 1j

    m1, op, m2 = item.split()
    if root:
        return evaluate(monkeys[m1]), evaluate(monkeys[m2])

    return ops[op](evaluate(monkeys[m1]), evaluate(monkeys[m2]))


if __name__ == "__main__":
    data = read_file("data/21.txt")[:-1]
    monkeys = {}
    for d in data:
        name, eqn = d.split(":")
        monkeys[name] = eqn.strip()

    print(evaluate(monkeys["root"]))

    monkeys["humn"] = "1j"

    lhs, rhs = evaluate(monkeys["root"], root=True)
    print((rhs - lhs.real) / lhs.imag)
