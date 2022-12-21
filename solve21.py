from aocd import submit, get_data


ops = {
    "+": lambda x, y: x+y,
    "-": lambda x, y: x-y,
    "*": lambda x, y: x*y,
    "/": lambda x, y: x//y,
    "=": lambda x, y: x == y,
    "^": lambda x, y: x ** y
}

def main():
    day = 21
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""": 152,
    }
    test_data_b = {
"""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""": 301,
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
    monkeys = {}
    togo = []

    for line in data.splitlines():
        sline = line.split()
        name = sline[0][:-1]
        try:
            monkeys[name] = int(sline[1])
        except Exception:
            togo.append((name, sline[2], sline[1], sline[3]))

    while togo:
        name, op, m0, m1 = togo.pop(0)
        if m0 in monkeys and m1 in monkeys:
            monkeys[name] = ops[op](monkeys[m0], monkeys[m1])
            if name == "root":
                return monkeys[name]
        else:
            togo.append((name, op, m0, m1))


def solve_b(data):
    monkeys = {}
    togo = []

    for line in data.splitlines():
        sline = line.split()
        name = sline[0][:-1]
        try:
            monkeys[name] = int(sline[1])
        except Exception:
            togo.append((name, sline[2], sline[1], sline[3]))

    # name, op-lambda, firstVar, secondVar, op-str
    sort = []
    while togo:
        # m = togo.pop(0)
        name, op, m0, m1 = togo.pop(0)
        if m0 in monkeys and m1 in monkeys:
            monkeys[name] = ops[op](monkeys[m0], monkeys[m1])
            if name == "root":
                sort.append((name, ops["="], m0, m1, "="))
                break
            sort.append((name, ops[op], m0, m1, op))

        else:
            togo.append((name, op, m0, m1))

    tree = ["root"]
    getParents(sort, "root", tree)
    result = []
    while tree:
        if isinstance(tree[0], str):
            if tree[0] == "humn":
                tree.pop(0)
        else:
            tree = tree[0]
            op = tree.pop(0)
            if isIn(tree[0], "humn"):
                if op == "+":
                    op = "-"
                elif op == "-":
                    op = "+"
                elif op == "*":
                    op = "/"
                elif op == "/":
                    op = "*"
                elif op == "=":
                    pass
                else:
                    raise NotImplementedError()
                if op == "=":
                    assert not result
                    result = tree.pop(1)
                else:
                    result = [op, result, tree.pop(1)]
            elif isIn(tree[1], "humn"):
                if op == "=":
                    assert not result
                    result = tree.pop(0)
                elif op == "+":
                    op = "-"
                    result = [op, result, tree.pop(0)]
                elif op == "-":
                    op = "-"
                    result = ["*", -1, [op, result, tree.pop(0)]]
                elif op == "*":
                    op = "/"
                    result = [op, result, tree.pop(0)]
                elif op == "/":
                    op = "*"
                    result = ["^", [op, result, tree.pop(0)], -1]
                elif op == "=":
                    pass
                    result = [op, result, tree.pop(0)]
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError()

    return evalTree(result, monkeys)


def getParents(sort, start, tree):
    try:
        op, m0, m1 = next((op, m0, m1) for s, _, m0, m1, op in sort if s == start)
    except StopIteration:
        return
    replaceInTree(tree, start, op, m0, m1)

    getParents(sort, m0, tree)
    getParents(sort, m1, tree)


def replaceInTree(tree, start, op, m0, m1):
    if isinstance(tree[0], list):
        replaceInTree(tree[0], start, op, m0, m1)
    else:
        if tree[0] == start:
            tree[0] = [op, m0, m1]
            return
    if len(tree) > 1:
        if isinstance(tree[1], list):
            replaceInTree(tree[1], start, op, m0, m1)
        else:
            if tree[1] == start:
                tree[1] = [op, m0, m1]
    if len(tree) > 2:
        if isinstance(tree[2], list):
            replaceInTree(tree[2], start, op, m0, m1)
        else:
            if tree[2] == start:
                tree[2] = [op, m0, m1]


def isIn(tree, start):
    if isinstance(tree, list):
        return any(isIn(t, start) for t in tree)
    return tree == start


def evalTree(tree, monkeys):
    if len(tree) == 3:
        t1 = tree[1]
        if not isinstance(t1, int):
            t1 = evalTree(t1, monkeys)
        t2 = tree[2]
        if not isinstance(t2, int):
            t2 = evalTree(t2, monkeys)
        return ops[tree[0]](t1, t2)
    else:
        if len(tree) == 1:
            if isinstance(tree[0], int):
                return tree[0]
            return monkeys[tree[0]]
        else:
            if isinstance(tree, int):
                return tree[0]
            return monkeys[tree]


if __name__ == "__main__":
    main()
