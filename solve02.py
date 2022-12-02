from aocd import submit, get_data


def main():
    day = 2
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """A Y
B X
C Z""": 15,
    }
    test_data_b = {
        """A Y
B X
C Z""": 12,
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
    opponents = ["A", "B", "C"]
    mes = ["X", "Y", "Z"]
    for line in data.splitlines():
        opponent, me = line.split()
        round = (mes.index(me) - opponents.index(opponent)) % len(opponents)
        if round == 1:
            # won
            result = 6
        elif round == 0:
            # draw
            result = 3
        else:
            # loss
            result = 0
        res += result + (mes.index(me) + 1)

    return res


def solve_b(data):
    res = 0
    opponents = ["A", "B", "C"]
    results = ["X", "Y", "Z"]
    for line in data.splitlines():
        opponent, target = line.split()
        target = results.index(target)
        if target == 0:
            # loose
            res += 0 + ((opponents.index(opponent) - 1) % len(opponents)) + 1
        elif target == 1:
            # draw
            res += 3 + opponents.index(opponent) + 1
        else:
            # win
            res += 6 + ((opponents.index(opponent) + 1) % len(opponents)) + 1
    return res


if __name__ == "__main__":
    main()
