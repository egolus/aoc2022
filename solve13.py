from itertools import zip_longest
from functools import cmp_to_key
from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 13
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""": 13,
    }
    test_data_b = {
        """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""": 140,
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


def compare(a, b):
    if a is None:
        return True
    if b is None:
        return False
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return True
        elif a > b:
            return False
        return None
    elif isinstance(a, str) and isinstance(b, str):
        return compare(int(a), int(b))
    elif isinstance(a, (int, str)):
        return compare([a], b)
    elif isinstance(b, (int, str)):
        return compare(a, [b])
    elif isinstance(a, list) and isinstance(b, list):
        for ax, bx in zip_longest(a, b):
            check = compare(ax, bx)
            if check is None:
                continue
            else:
                return check


def compare2(a, b):
    check = compare(a, b)
    if check:
        return -1
    return 1


def solve_a(data):
    res = []
    for i, pair in enumerate(data.split("\n\n")):
        a, b = pair.splitlines()
        a = eval(a)
        b = eval(b)
        if compare(a, b):
            res.append(i+1)

    return sum(res)


def solve_b(data):
    packets = [[[2]], [[6]]]
    for line in data.splitlines():
        if line:
            packets.append(eval(line))

    packets = sorted(packets, key=cmp_to_key(compare2))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


if __name__ == "__main__":
    main()
