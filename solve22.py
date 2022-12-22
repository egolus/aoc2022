from aocd import submit, get_data


def main():
    day = 22
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""": 6032,
    }
    test_data_b = {
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
    grid = {}
    path = ""
    position = None
    directions = ("R", "D", "L", "U")
    direction = "R"
    pathposition = 0

    for y, line in enumerate(data.split("\n\n")[0].splitlines()):
        for x, c in enumerate(line):
            if c != " ":
                grid[(y, x)] = c
                if not position:
                    position = (y, x)
    path = data.split("\n\n")[1]

    minx = min(x for y, x in grid)
    maxx = max(x for y, x in grid)
    miny = min(y for y, x in grid)
    maxy = max(y for y, x in grid)

    while pathposition < len(path):
        try:
            nextL = path.index("L", pathposition)
        except ValueError:
            nextL = len(path)
        try:
            nextR = path.index("R", pathposition)
        except ValueError:
            nextR = len(path)
        newpathpos = min(nextL, nextR)
        steps = int(path[pathposition:newpathpos])
        pathposition = newpathpos+1

        # move number of steps or until we hit a wall
        for s in range(steps):
            y, x = position
            if direction == "L":
                newpos = (y, x-1)
            elif direction == "R":
                newpos = (y, x+1)
            elif direction == "U":
                newpos = (y-1, x)
            elif direction == "D":
                newpos = (y+1, x)

            if newpos not in grid:
                if direction == "R":
                    for x in range(minx, maxx-1):
                        if (newpos[0], x) in grid:
                            newpos = (newpos[0], x)
                            break
                elif direction == "L":
                    for x in range(maxx, minx, -1):
                        if (newpos[0], x) in grid:
                            newpos = (newpos[0], x)
                            break
                elif direction == "D":
                    for y in range(miny, maxy-1):
                        if (y, newpos[1]) in grid:
                            newpos = (y, newpos[1])
                            break
                elif direction == "U":
                    for y in range(maxy, miny, -1):
                        if (y, newpos[1]) in grid:
                            newpos = (y, newpos[1])
                            break
            if grid[newpos] == ".":
                position = newpos
            elif grid[newpos] == "#":
                break

        # turn clockwise (R) or counterclockwise (L)
        if newpathpos == len(path):
            break
        if path[newpathpos] == "L":
            direction = directions[(directions.index(direction)-1) % len(directions)]
        if path[newpathpos] == "R":
            direction = directions[(directions.index(direction)+1) % len(directions)]
        pathposition = newpathpos+1

    return 1000*(position[0]+1) + 4*(position[1]+1) + directions.index(direction)


def calculateBorders(grid):
    maxy = max(y for y, x in grid)

    facelen = (maxy+1) // 4
    borders = {}

    # face 1
    # top -> face 6 left
    for s in range(facelen+1):
        borders[(-1, facelen + s)] = ((facelen*3 + s, 0), "R")
    # left -> face 4 left upside down
    for s in range(facelen+1):
        borders[(s, facelen-1)] = ((facelen*3 - 1 - s, 0), "R")

    # face 2
    # top -> face 6 bottom
    for s in range(facelen+1):
        borders[(-1, facelen*2 + s)] = ((facelen*4-1, s), "U")
    # right -> face 5 right upside down
    for s in range(facelen+1):
        borders[(s, facelen*3)] = ((facelen*3 - 1 - s, facelen*2 - 1), "L")
    # bottom -> face 3 right
    for s in range(facelen+1):
        borders[(facelen, facelen*2 + s)] = ((facelen + s, facelen*2 - 1), "L")

    # face 3
    # left -> face 4 top
    for s in range(facelen+1):
        borders[(facelen + s, facelen - 1)] = ((facelen*2, s), "D")
    # right -> face 2 bottom
    for s in range(facelen+1):
        borders[(facelen + s, facelen*2)] = ((facelen - 1, facelen*2 + s), "U")

    # face 4
    # top -> face 3 left
    for s in range(facelen+1):
        borders[(facelen*2 - 1, s)] = ((facelen + s, facelen), "R")
    # left -> face 1 left upside down
    for s in range(facelen+1):
        borders[(facelen*2 + s, -1)] = ((facelen - 1 - s, facelen), "R")

    # face 5
    # right -> face 2 right upside down
    for s in range(facelen+1):
        borders[(facelen*2 + s, facelen*2)] = ((facelen - 1 - s, facelen*3 - 1), "L")
    # bottom -> face 6 right
    for s in range(facelen+1):
        borders[(facelen*3, facelen + s)] = ((facelen*3 + s, facelen - 1), "L")

    # face 6
    # left -> face 1 top
    for s in range(facelen+1):
        borders[(facelen*3 + s, -1)] = ((0, facelen + s), "D")
    # right -> face 5 bottom
    for s in range(facelen+1):
        borders[(facelen*3 + s, facelen)] = ((facelen*3 - 1, facelen + s), "U")
    # bottom -> face 2 top
    for s in range(facelen+1):
        borders[(facelen*4, s)] = ((0, facelen*2 + s), "D")

    return borders


def solve_b(data):
    grid = {}
    path = ""
    position = None
    directions = ("R", "D", "L", "U")
    direction = "R"
    pathposition = 0

    for y, line in enumerate(data.split("\n\n")[0].splitlines()):
        for x, c in enumerate(line):
            if c != " ":
                grid[(y, x)] = c
                if not position:
                    position = (y, x)
    path = data.split("\n\n")[1]

    minx = min(x for y, x in grid)
    maxx = max(x for y, x in grid)
    miny = min(y for y, x in grid)
    maxy = max(y for y, x in grid)

    borders = calculateBorders(grid)

    while pathposition < len(path):
        try:
            nextL = path.index("L", pathposition)
        except ValueError:
            nextL = len(path)
        try:
            nextR = path.index("R", pathposition)
        except ValueError:
            nextR = len(path)
        newpathpos = min(nextL, nextR)
        steps = int(path[pathposition:newpathpos])
        pathposition = newpathpos+1

        # move number of steps or until we hit a wall
        for s in range(steps):
            y, x = position
            if direction == "L":
                newpos = (y, x-1)
            elif direction == "R":
                newpos = (y, x+1)
            elif direction == "U":
                newpos = (y-1, x)
            elif direction == "D":
                newpos = (y+1, x)

            if newpos not in grid:
                newpos, newdirection = borders[newpos]
                if grid[newpos] == ".":
                    position = newpos
                    direction = newdirection
                elif grid[newpos] == "#":
                    break
            else:
                if grid[newpos] == ".":
                    position = newpos
                elif grid[newpos] == "#":
                    break

        # turn clockwise (R) or counterclockwise (L)
        if newpathpos == len(path):
            break
        if path[newpathpos] == "L":
            direction = directions[(directions.index(direction)-1) % len(directions)]
        if path[newpathpos] == "R":
            direction = directions[(directions.index(direction)+1) % len(directions)]
        pathposition = newpathpos+1

    return 1000*(position[0]+1) + 4*(position[1]+1) + directions.index(direction)


if __name__ == "__main__":
    main()
