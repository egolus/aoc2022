from aocd import submit, get_data


def main():
    day = 14
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""": 24,
    }
    test_data_b = {
        """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""": 93,
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


def poureSand(grid, y=0, x=500, miny=None, minx=None, maxy=None, maxx=None):
    starty = y
    startx = x
    while y <= maxy:
        # down
        while y <= maxy:
            if (y+1, x) in grid:
                break
            y += 1
        else:
            return

        # down left
        if (y+1, x-1) not in grid:
            y += 1
            x -= 1
            continue

        # down right
        if (y+1, x+1) not in grid:
            y += 1
            x += 1
            continue

        grid[(y, x)] = "o"
        y, x = starty, startx


def poureSand_b(grid, y=0, x=500, miny=None, minx=None, maxy=None, maxx=None):
    starty = y
    startx = x
    while True:
        # down
        while y <= maxy:
            if (y+1, x) in grid:
                break
            y += 1

        # down left
        if y <= maxy and (y+1, x-1) not in grid:
            y += 1
            x -= 1
            continue

        # down right
        if y <= maxy and (y+1, x+1) not in grid:
            y += 1
            x += 1
            continue

        grid[(y, x)] = "o"
        if (y, x) == (starty, startx):
            break
        y, x = starty, startx


def solve_a(data):
    grid = {(0, 500): "+"}

    for line in data.splitlines():
        sline = line.split(" -> ")
        for i in range(1, len(sline)):
            x0, y0 = [int(s) for s in sline[i-1].split(",")]
            x1, y1 = [int(s) for s in sline[i].split(",")]

            if y0 > y1:
                ystep = -1
            else:
                ystep = +1
            if x0 > x1:
                xstep = -1
            else:
                xstep = +1
            for ys in range(y0, y1 + ystep, ystep):
                for xs in range(x0, x1 + xstep, xstep):
                    grid[(ys, xs)] = "#"

    minx = min(x for (_, x) in grid)
    miny = min(y for (y, _) in grid)
    maxx = max(x for (_, x) in grid)
    maxy = max(y for (y, _) in grid)

    poureSand(grid, miny=miny, minx=minx, maxy=maxy, maxx=maxx)
    return len([v for v in grid.values() if v == "o"])


def solve_b(data):
    grid = {(0, 500): "+"}

    for line in data.splitlines():
        sline = line.split(" -> ")
        for i in range(1, len(sline)):
            x0, y0 = [int(s) for s in sline[i-1].split(",")]
            x1, y1 = [int(s) for s in sline[i].split(",")]

            if y0 > y1:
                ystep = -1
            else:
                ystep = +1
            if x0 > x1:
                xstep = -1
            else:
                xstep = +1
            for ys in range(y0, y1 + ystep, ystep):
                for xs in range(x0, x1 + xstep, xstep):
                    grid[(ys, xs)] = "#"

    minx = min(x for (_, x) in grid) - 10
    miny = min(y for (y, _) in grid)
    maxx = max(x for (_, x) in grid) + 10
    maxy = max(y for (y, _) in grid)

    poureSand_b(grid, miny=miny, minx=minx, maxy=maxy, maxx=maxx)
    return len([v for v in grid.values() if v == "o"])


if __name__ == "__main__":
    main()
