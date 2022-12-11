from functools import reduce
from operator import mul
from aocd import submit, get_data


def main():
    day = 11
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""": 10605,
    }
    test_data_b = {
        """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""": 2713310158,
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
    monkeys = []
    ms = data.split("\n\n")
    for m in ms:
        items = []
        op = None
        test = None
        dirs = {}
        for line in m.splitlines():
            if line.startswith("Monkey"):
                pass
            elif line.startswith("  Starting"):
                items = [int(x) for x in line.split(": ")[1].split(", ")]
            elif line.startswith("  Operation"):
                sop = line[19:].split()
                for i, x in enumerate(sop):
                    try:
                        sop[i] = int(x)
                    except Exception:
                        pass
                if sop[1] == "+":
                    plus = lambda x: x[0] + x[1]
                    if type(sop[0]) == int:
                        op = [plus, sop[0]]
                    elif type(sop[2]) == int:
                        op = [plus, sop[2]]
                    else:
                        op = [plus]
                elif sop[1] == "*":
                    mul = lambda x: x[0] * x[1]
                    if type(sop[0]) == int:
                        op = [mul, sop[0]]
                    elif type(sop[2]) == int:
                        op = [mul, sop[2]]
                    else:
                        def mulX(x):
                            return x * x
                        op = [mul]
            elif line.startswith("  Test"):
                test = int(line[20:])
            elif line.startswith("    If true"):
                dirs[True] = int(line[29:])
            elif line.startswith("    If false"):
                dirs[False] = int(line[29:])
        monkeys.append({
            "items": items,
            "op": op,
            "test": test,
            "dirs": dirs,
            "insp": 0,
        })

    for round in range(20):
        for m in monkeys:
            while m["items"]:
                m["insp"] += 1
                it = m["items"].pop(0)
                it = m["op"][0]((it, m["op"][1] if len(m["op"]) > 1 else it)) // 3
                if not it % m["test"]:
                    monkeys[m["dirs"][True]]["items"].append(it)
                else:
                    monkeys[m["dirs"][False]]["items"].append(it)
    times = sorted([m["insp"] for m in monkeys], reverse=True)
    return times[0] * times[1]


def solve_b(data):
    monkeys = []
    ms = data.split("\n\n")
    for m in ms:
        items = []
        op = None
        test = None
        dirs = {}
        for line in m.splitlines():
            if line.startswith("Monkey"):
                pass
            elif line.startswith("  Starting"):
                items = [int(x) for x in line.split(": ")[1].split(", ")]
            elif line.startswith("  Operation"):
                sop = line[19:].split()
                for i, x in enumerate(sop):
                    try:
                        sop[i] = int(x)
                    except Exception:
                        pass
                if sop[1] == "+":
                    plus = lambda x: x[0] + x[1]
                    if type(sop[0]) == int:
                        op = [plus, sop[0]]
                    elif type(sop[2]) == int:
                        op = [plus, sop[2]]
                    else:
                        op = [plus]
                elif sop[1] == "*":
                    mult = lambda x: x[0] * x[1]
                    if type(sop[0]) == int:
                        op = [mult, sop[0]]
                    elif type(sop[2]) == int:
                        op = [mult, sop[2]]
                    else:
                        def mulX(x):
                            return x * x
                        op = [mult]
            elif line.startswith("  Test"):
                test = int(line[20:])
            elif line.startswith("    If true"):
                dirs[True] = int(line[29:])
            elif line.startswith("    If false"):
                dirs[False] = int(line[29:])
        monkeys.append({
            "items": items,
            "op": op,
            "test": test,
            "dirs": dirs,
            "insp": 0,
        })

    for round in range(10_000):
        for m in monkeys:
            while m["items"]:
                m["insp"] += 1
                it = m["items"].pop(0)
                it = m["op"][0]((it, m["op"][1] if len(m["op"]) > 1 else it))
                if not it % m["test"]:
                    monkeys[m["dirs"][True]]["items"].append(
                            it % reduce(mul, [x["test"] for x in monkeys]))
                else:
                    monkeys[m["dirs"][False]]["items"].append(
                            it % reduce(mul, [x["test"] for x in monkeys]))
    times = sorted([m["insp"] for m in monkeys], reverse=True)
    return times[0] * times[1]


if __name__ == "__main__":
    main()
