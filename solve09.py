from aocd import submit, get_data


def main():
    day = 9
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""": 13,
    }
    test_data_b = {
        """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""": 1,
        """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""": 36,
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
    positions = {(0, 0)}
    head = (0, 0)
    tail = (0, 0)

    for line in data.splitlines():
        direction, steps = line.split()
        steps = int(steps)

        for i in range(steps):
            if direction == "U":
                # up
                head = (head[0], head[1] - 1)
            elif direction == "D":
                # down
                head = (head[0], head[1] + 1)
            elif direction == "L":
                # left
                head = (head[0] - 1, head[1])
            elif direction == "R":
                # right
                head = (head[0] + 1, head[1])

            if (
                    head[0] > tail[0] + 1 or
                    head[0] < tail[0] - 1 or
                    head[1] > tail[1] + 1 or
                    head[1] < tail[1] - 1
                    ):
                if head[0] > tail[0]:
                    tail = (tail[0] + 1, tail[1])
                elif head[0] < tail[0]:
                    tail = (tail[0] - 1, tail[1])
                if head[1] > tail[1]:
                    tail = (tail[0], tail[1] + 1)
                elif head[1] < tail[1]:
                    tail = (tail[0], tail[1] - 1)
            positions.add(tail)

    return len(positions)


def solve_b(data):
    positions = {(0, 0)}
    knots = [(0, 0)] * 10

    for line in data.splitlines():
        direction, steps = line.split()
        steps = int(steps)

        for i in range(steps):
            if direction == "U":
                # up
                knots[0] = (knots[0][0], knots[0][1] - 1)
            elif direction == "D":
                # down
                knots[0] = (knots[0][0], knots[0][1] + 1)
            elif direction == "L":
                # left
                knots[0] = (knots[0][0] - 1, knots[0][1])
            elif direction == "R":
                # right
                knots[0] = (knots[0][0] + 1, knots[0][1])

            for i in range(1, len(knots)):
                if (
                        knots[i-1][0] > knots[i][0] + 1 or
                        knots[i-1][0] < knots[i][0] - 1 or
                        knots[i-1][1] > knots[i][1] + 1 or
                        knots[i-1][1] < knots[i][1] - 1
                        ):
                    if knots[i-1][0] > knots[i][0]:
                        knots[i] = (knots[i][0] + 1, knots[i][1])
                    elif knots[i-1][0] < knots[i][0]:
                        knots[i] = (knots[i][0] - 1, knots[i][1])
                    if knots[i-1][1] > knots[i][1]:
                        knots[i] = (knots[i][0], knots[i][1] + 1)
                    elif knots[i-1][1] < knots[i][1]:
                        knots[i] = (knots[i][0], knots[i][1] - 1)
            positions.add(knots[i])

    return len(positions)


if __name__ == "__main__":
    main()
