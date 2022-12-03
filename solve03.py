from aocd import submit, get_data


def main():
    day = 3
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
            """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""": 157,
    }
    test_data_b = {
            """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""": 70,
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
    chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    print(data)
    for line in data.splitlines():
        first, second = line[:len(line)//2], line[len(line)//2:]
        res.append(set(first).intersection(set(second)).pop())
    return sum([chars.index(c) for c in res])


def solve_b(data):
    chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    group = []
    res = []
    for i, line in enumerate(data.splitlines()):
        group.append(line)
        if i % 3 == 2:
            res.append(set(group[0]).intersection(group[1]).intersection(group[2]).pop())
            group.clear()
    return sum([chars.index(c) for c in res])


if __name__ == "__main__":
    main()
