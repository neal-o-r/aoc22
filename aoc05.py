from utils import read_file
from collections import namedtuple
import re


def parse(data):
    boxes = create_stacks(data[:8])
    instrs = list(map(parse_instruction, data[10:]))
    return boxes, instrs


def create_stacks(boxes):
    # split into columns
    n = len(boxes[0])
    inds = list(zip(range(0, n, 4), range(3, n + 1, 4)))
    split_towers = lambda b: [b[i:j] for i, j in inds]

    towers = map(split_towers, boxes)

    # transpose the towers
    stacks = zip(*towers)
    return [list(filter(lambda x: not x.isspace(), s)) for s in stacks]


def parse_instruction(instr):
    m = namedtuple("Move", ["n", "start", "end"])
    n, s, e = map(int, re.findall(r"\d+", instr))
    return m(n, s - 1, e - 1)


def apply_instr(stacks, instr):

    for _ in range(instr.n):
        box = stacks[instr.start].pop(0)
        stacks[instr.end].insert(0, box)

    return stacks


def apply_instr_2(stacks, instr):

    boxes = []
    for i in range(instr.n):
        boxes.append(stacks[instr.start].pop(0))

    stacks[instr.end] = boxes + stacks[instr.end]

    return stacks


if __name__ == "__main__":

    data = read_file("./data/05.txt")[:-1]

    stacks, instrs = parse(data)

    for i in instrs:
        stacks = apply_instr_2(stacks, i)

    print("".join([s[0][1] for s in stacks]))
