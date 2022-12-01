from aocd import submit, get_data


def main():
    day = 17
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        "": True,
    }
    test_data_b = {
        "": True,
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
    return res


def solve_b(data):
    res = 0
    return res


if __name__ == "__main__":
    main()
