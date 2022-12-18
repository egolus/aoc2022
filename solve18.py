from aocd import submit, get_data


def main():
    day = 18
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""": 64,
    }
    test_data_b = {
"""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""": 58,
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


def depth(grid, maxx, maxy, maxz):
    """ find all positions that are reachable from the outside """
    outside = set()
    tocheck = set()
    for y in range(-1, maxy+1):
        for z in range(-1, maxz+1):
            tocheck.add((-1, y, z))
            tocheck.add((maxx+1, y, z))
    for x in range(-1, maxx+1):
        for z in range(-1, maxz+1):
            tocheck.add((x, -1, z))
            tocheck.add((x, maxy+1, z))
    for x in range(-1, maxx+1):
        for y in range(-1, maxy+1):
            tocheck.add((x, y, -1))
            tocheck.add((x, y, maxz+1))
    walk(grid, outside, tocheck, maxx, maxy, maxz)
    return outside


def walk(grid, outside, tocheck, maxx, maxy, maxz):
    while tocheck:
        cube = tocheck.pop()
        if cube in outside or cube in grid:
            continue
        outside.add(cube)
        for neighbour in [
            (cube[0], cube[1], cube[2]-1),
            (cube[0], cube[1], cube[2]+1),

            (cube[0], cube[1]-1, cube[2]),
            (cube[0], cube[1]+1, cube[2]),

            (cube[0]-1, cube[1], cube[2]),
            (cube[0]+1, cube[1], cube[2]),
        ]:
            if (cube[0] < -1 or cube[1] < -1 or cube[2] < -1 or
                    cube[0] > maxx+1 or cube[1] > maxy+1 or cube[2] > maxz+1 or
                    neighbour in grid or neighbour in tocheck or neighbour in outside):
                continue
            else:
                tocheck.add(neighbour)


def connected(cube, outside):
    faces = 0
    # for group in outside:
    for neighbour in [
        (cube[0], cube[1], cube[2]-1),
        (cube[0], cube[1], cube[2]+1),

        (cube[0], cube[1]-1, cube[2]),
        (cube[0], cube[1]+1, cube[2]),

        (cube[0]-1, cube[1], cube[2]),
        (cube[0]+1, cube[1], cube[2]),
    ]:
        if neighbour in outside:
            faces += 1
    return faces


def solve_a(data):
    grid = set()
    sol = 0

    for line in data.splitlines():
        x, y, z = [int(c) for c in line.split(",")]
        grid.add((x, y, z))

    for cube in grid:
        for neighbour in [
            (cube[0], cube[1], cube[2]-1),
            (cube[0], cube[1], cube[2]+1),

            (cube[0], cube[1]-1, cube[2]),
            (cube[0], cube[1]+1, cube[2]),

            (cube[0]-1, cube[1], cube[2]),
            (cube[0]+1, cube[1], cube[2]),
        ]:
            if neighbour not in grid:
                sol += 1
    return sol


def solve_b(data):
    grid = set()
    sol = 0

    for line in data.splitlines():
        x, y, z = [int(c) for c in line.split(",")]
        grid.add((x, y, z))

    maxx = max(x for (x, y, z) in grid)
    maxy = max(y for (x, y, z) in grid)
    maxz = max(z for (x, y, z) in grid)

    outside = depth(grid, maxx, maxy, maxz)
    sol = sum(connected(cube, outside) for cube in grid)
    return sol


if __name__ == "__main__":
    main()
