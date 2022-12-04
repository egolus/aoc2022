from aocd import submit, get_data


def main():
    day = 4
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
            """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""": 2,
    }
    test_data_b = {
            """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""": 4,
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
    res = 0
    for line in data.splitlines():
        a, b = line.split(",")
        a0, a1 = [int(x) for x in a.split("-")]
        b0, b1 = [int(x) for x in b.split("-")]
        if ((a0 <= b0) and (a1 >= b1)) or ((a0 >= b0) and (a1 <= b1)):
            res += 1
    return res


def solve_b(data):
    res = 0
    for line in data.splitlines():
        a, b = line.split(",")
        a0, a1 = [int(x) for x in a.split("-")]
        b0, b1 = [int(x) for x in b.split("-")]
        if (
            (a0 <= b0 and a1 >= b0) or
            (a1 >= b1 and a0 <= b1) or
            (b0 <= a0 and b1 >= a0) or
            (b1 >= a1 and b0 <= a1)
        ):
            res += 1
    return res


if __name__ == "__main__":
    main()
