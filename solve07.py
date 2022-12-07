from aocd import submit, get_data


def main():
    day = 7
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""": 95437,
    }
    test_data_b = {
        """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""": 24933642,

    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    stack = {}
    position = []
    maxsize = 100_000

    for line in data.splitlines():
        if line.startswith("$ cd"):
            if line == "$ cd ..":
                position.pop()
            elif line.startswith("$ cd /"):
                position = [line[5:]]
                stack[tuple(position)] = {"type": "d", "children": []}
            else:
                position.append(line[5:])
                stack[tuple(position)] = {"type": "d", "children": []}
        if line.startswith("$"):
            continue
        else:
            size, name = line.split()
            stack[tuple(position)]["children"].append(name)
            try:
                size = int(size)
                stack[tuple([*position, name])] = {"type": "f", "size": size}
            except Exception:
                pass

    position = ["/"]
    getSize(stack, position)

    res = 0
    for k, v in stack.items():
        if v["type"] == "d" and v["size"] <= maxsize:
            res += v["size"]
    return res


def getSize(stack, key):
    size = 0
    if stack[tuple(key)]["type"] == "d":
        for child in stack[tuple(key)]["children"]:
            size += getSize(stack, [*key, child])
        stack[tuple(key)]["size"] = size
    else:
        size += stack[tuple(key)]["size"]
    return size


def solve_b(data):
    stack = {}
    position = []
    maxsize = 70_000_000
    needed = 30_000_000

    for line in data.splitlines():
        if line.startswith("$ cd"):
            if line == "$ cd ..":
                position.pop()
            elif line.startswith("$ cd /"):
                position = [line[5:]]
                stack[tuple(position)] = {"type": "d", "children": []}
            else:
                position.append(line[5:])
                stack[tuple(position)] = {"type": "d", "children": []}
        if line.startswith("$"):
            continue
        else:
            size, name = line.split()
            stack[tuple(position)]["children"].append(name)
            try:
                size = int(size)
                stack[tuple([*position, name])] = {"type": "f", "size": size}
            except Exception:
                pass

    position = ["/"]
    getSize(stack, position)

    available = maxsize - stack[("/",)]["size"]
    for k, v in sorted([(k, v) for k, v in stack.items() if v["type"] == "d"],
                       key=lambda x: x[1]["size"]):
        if v["size"] > needed - available:
            return v["size"]


if __name__ == "__main__":
    main()
