from collections import defaultdict
from utils import read_file


def to_path(lst):
    return "/".join(lst)


def directory_map(data):

    path = ["~"]
    directories = set("~")
    files = defaultdict(list)

    for line in data:
        if line.startswith("$ cd"):
            _, _, loc = line.split()
            if loc == "/":
                path = ["~"]
            elif loc == "..":
                path.pop()
            else:
                path.append(loc)
                directories.add(to_path(path))

        elif line[0].isdigit():
            s, _ = line.split()
            files[to_path(path)] += [int(s)]

    return files, directories


def sum_under(path, files):
    return sum(sum(v) for k, v in files.items() if path in k)


if __name__ == "__main__":

    data = read_file("./data/07.txt")[:-1]

    file_sizes, dirs = directory_map(data)

    dir_sizes = {d: sum_under(d, file_sizes) for d in dirs}

    print(sum(v for _, v in dir_sizes.items() if v < 100_000))

    total_disk_space = 70000000

    needed = 30000000
    used = dir_sizes["~"]
    free = total_disk_space - used

    to_free = needed - free

    print(min(v for _, v in dir_sizes.items() if v > to_free))
