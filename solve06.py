from aocd import submit, get_data


def main():
    day = 6
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }
    test_data_b = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
        "nppdvjthqldpwncqszvftbrmjlhg": 23,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
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
    for i, c in enumerate(data):
        if len(set(data[i:i+4])) == 4:
            return i + 4


def solve_b(data):
    for i, c in enumerate(data):
        if len(set(data[i:i+14])) == 14:
            return i + 14


if __name__ == "__main__":
    main()
