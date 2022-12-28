from utils import read_file
from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.nxt = None
        self.prv = None

    def __repr__(self):
        return str(self.val)


class CLL:
    def __init__(self, lst):
        self.n = len(lst)
        self._nodes = [Node(l) for l in lst]

        for i, n in enumerate(self._nodes):
            n.nxt = self._nodes[(i + 1) % self.n]
            n.prv = self._nodes[i - 1]

        self.head = self._nodes[0]

    def __repr__(self):
        repr = ""
        n = self.head
        for _ in range(self.n):
            repr += n.__repr__() + " <--> "
            n = n.nxt

        return repr

    def rotate(self, steps):
        if steps < 0:
            new_head = self.head.nxt
            for _ in range((-steps - 1) % (self.n - 1)):
                new_head = new_head.nxt
            self.head = new_head
        elif steps > 0:
            new_head = self.head.prv
            for _ in range((steps - 1) % (self.n - 1)):
                new_head = new_head.prv
            self.head = new_head

    def pop(self):
        # take the head item off the list
        self.n -= 1

        popped = self.head
        self.head = popped.nxt
        self.head.prv = popped.prv
        popped.prv.nxt = self.head
        return popped.val

    def add(self, val):
        # put a head on the list
        n = Node(val)
        self.n += 1
        n.prv = self.head.prv
        self.head.prv.nxt = n
        self.head.prv = n
        n.nxt = self.head
        self.head = n

    def index(self, val):
        n = self.head
        for i in range(self.n):
            if n.val == val:
                return i
            n = n.nxt

    def rotate_to(self, val):
        i = self.index(val)
        assert i is not None, "Index not found!"
        self.rotate(-i)

    def get_index(self, i):
        t = self.head
        for _ in range(i):
            t = t.nxt
        return t.val


def mix(circ, enc):
    n = len(enc)
    for i, v in enumerate(enc):
        circ.rotate_to((i, v))
        val = circ.pop()
        circ.rotate(-v % (n - 1))
        circ.add(val)

    return circ


if __name__ == "__main__":
    data = read_file("data/20.txt")[:-1]
    enc = list(map(int, data))

    circ = CLL(list(enumerate(enc)))
    mixed = mix(circ, enc)

    mixed.rotate_to((87, 0))

    print(sum(mixed.get_index(i)[1] for i in [1000, 2000, 3000]))

    enc = [e * 811589153 for e in enc]

    circ = CLL(list(enumerate(enc)))
    mixed = mix(circ, enc)
    for _ in range(9):
        mixed = mix(mixed, enc)

    mixed.rotate_to((87, 0))

    print(sum(mixed.get_index(i)[1] for i in [1000, 2000, 3000]))
