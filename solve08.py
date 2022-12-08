from aocd import submit, get_data


def main():
    day = 8
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """30373
25512
65332
33549
35390""": 21,
    }
    test_data_b = {
        """30373
25512
65332
33549
35390""": 8,
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
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(y, x)] = int(c)

    maxy, maxx = y, x

    for y in range(maxy+1):
        for x in range(maxx+1):
            visible = True
            # top
            y2 = y
            while y2 >= 0:
                y2 -= 1
                if (y2, x) in grid and grid[(y2, x)] >= grid[(y, x)]:
                    visible = False
                    break
            else:
                res += 1
                continue
            # bottom
            y2 = y
            while y2 <= maxy:
                y2 += 1
                if (y2, x) in grid and grid[(y2, x)] >= grid[(y, x)]:
                    visible = False
                    break
            else:
                res += 1
                continue
            # left
            x2 = x
            while x2 >= 0:
                x2 -= 1
                if (y, x2) in grid and grid[(y, x2)] >= grid[(y, x)]:
                    visible = False
                    break
            else:
                res += 1
                continue
            # right
            x2 = x
            while x2 <= maxx:
                x2 += 1
                if (y, x2) in grid and grid[(y, x2)] >= grid[(y, x)]:
                    visible = False
                    break
            else:
                res += 1
                continue

            if visible:
                res += 1
    return res


def solve_b(data):
    res = 0
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(y, x)] = int(c)

    maxy, maxx = y, x

    for y in range(1, maxy):
        for x in range(1, maxx):
            score = 1
            # top
            y2 = y
            while y2 >= 0:
                y2 -= 1
                if (y2, x) in grid and (grid[(y2, x)] >= grid[(y, x)] or y2 == 0):
                    score *= y - y2
                    break
            # bottom
            y2 = y
            while y2 <= maxy:
                y2 += 1
                if (y2, x) in grid and (grid[(y2, x)] >= grid[(y, x)] or y2 == maxy):
                    score *= y2 - y
                    break
            # left
            x2 = x
            while x2 >= 0:
                x2 -= 1
                if (y, x2) in grid and (grid[(y, x2)] >= grid[(y, x)] or x2 == 0):
                    score *= x - x2
                    break
            # right
            x2 = x
            while x2 <= maxx:
                x2 += 1
                if (y, x2) in grid and (grid[(y, x2)] >= grid[(y, x)] or x2 == maxx):
                    score *= x2 - x
                    break

            if score > res:
                res = score
    return res


if __name__ == "__main__":
    main()
