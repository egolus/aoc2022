from aocd import submit, get_data


def main():
    day = 20
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""1
2
-3
3
-2
0
4""": 3,
    }
    test_data_b = {
"""1
2
-3
3
-2
0
4""": 1623178306,
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
    numbers = [int(line) for line in data.splitlines()]
    indices = list(range(len(numbers)))
    for i, n in enumerate(numbers):
        newpos = (indices.index(i) + n)
        indices.remove(i)
        indices.insert(newpos % len(indices), i)

    start = indices.index(numbers.index(0))
    return (numbers[indices[(start+1000) % len(indices)]] +
            numbers[indices[(start+2000) % len(indices)]] +
            numbers[indices[(start+3000) % len(indices)]])


def solve_b(data):
    key = 811589153
    numbers = [int(line) * key for line in data.splitlines()]
    indices = list(range(len(numbers)))
    for r in range(10):
        for i, n in enumerate(numbers):
            newpos = (indices.index(i) + n)
            indices.remove(i)
            indices.insert(newpos % len(indices), i)

    start = indices.index(numbers.index(0))
    return (numbers[indices[(start+1000) % len(indices)]] +
            numbers[indices[(start+2000) % len(indices)]] +
            numbers[indices[(start+3000) % len(indices)]])


if __name__ == "__main__":
    main()
