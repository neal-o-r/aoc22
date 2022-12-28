import re
from collections import namedtuple, Counter
from math import prod

Monkey = namedtuple("Monkey", "n, items, op, arg, test, t, f")


def parse_monkey(txt):
    regex = """Monkey (\d+):
  Starting items: (.+)
  Operation: new = old (.) (.+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""
    name, items, op, arg, test, throw_t, throw_f = re.findall(regex, txt)[0]
    return Monkey(
        name, list(map(int, items.split(","))), op, arg, int(test), throw_t, throw_f
    )


def inspect(item, monkey):
    # index an item should go to
    arg = monkey.arg if not monkey.arg == "old" else item

    worry = eval(f"{item} {monkey.op} {arg}") % 9699690
    if not eval(f"{worry} % {monkey.test}"):
        return worry, int(monkey.t)
    else:
        return worry, int(monkey.f)


def throw(monkey, monkeys, inspected):
    while monkey.items:
        item = monkey.items.pop(0)
        worry, indx = inspect(item, monkey)
        monkeys[indx].items.append(worry)
        inspected[monkey.n] += 1

    return monkeys, inspected


def play_round(monkeys, inspected):
    for m in monkeys:
        monkeys, inspected = throw(m, monkeys, inspected)

    return monkeys, inspected


if __name__ == "__main__":
    data = open("data/11.txt").read().split("\n\n")
    monkeys = list(map(parse_monkey, data))

    inspected = Counter()
    for i in range(20):
        _, inspected = play_round(monkeys, inspected)

    print(prod(i[1] for i in inspected.most_common(2)))

    inspected = Counter()
    for i in range(10_000):
        _, inspected = play_round(monkeys, inspected)

    print(prod(i[1] for i in inspected.most_common(2)))
