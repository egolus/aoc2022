from aocd import submit, get_data


def main():
    day = 1
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""": 24000,
    }
    test_data_b = {
        """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""": 45000,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    res = 0
    cals = 0
    for line in data.splitlines():
        if line:
            cals += int(line)
        else:
            res = max(res, cals)
            cals = 0
    res = max(res, cals)
    return res


def solve_b(data):
    elves = []
    cals = 0
    for line in data.splitlines():
        if line:
            cals += int(line)
        else:
            elves.append(cals)
            cals = 0
    elves.append(cals)
    return sum(sorted(elves, reverse=True)[:3])


if __name__ == "__main__":
    main()
