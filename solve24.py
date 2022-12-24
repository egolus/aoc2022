from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 24
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""": 18,
    }
    test_data_b = {
"""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""": 54,
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


def drawMap(blizzardPositions, blizzardDirections, positions, maxx, maxy):
    for y in range(maxy+2):
        for x in range(maxx+2):
            if (y, x) in positions:
                print("E", end="")
            elif (le := len([b for b in blizzardPositions if (y, x) == b])) > 1:
                print(le, end="")
            elif len([b for b in blizzardPositions if (y, x) == b]) == 1:
                print(blizzardDirections[
                    next(k for k, v in enumerate(blizzardPositions)
                         if (y, x) == v)], end="")
            elif y == 0 or x == 0 or y == maxy+1 or x == maxx+1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


def solve_a(data):
    grid = {}
    blizzardPositions = []
    blizzardDirections = []
    start = (0, 1)
    positions = [start]

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                # wall
                grid[(y, x)] = "#"
            if c in (">", "<", "v", "^"):
                # blizzard
                blizzardPositions.append((y, x))
                blizzardDirections.append(c)

    minx = min(x for (y, x) in grid) + 1
    miny = min(y for (y, x) in grid) + 1
    maxx = max(x for (y, x) in grid) - 1
    maxy = max(y for (y, x) in grid) - 1

    goal = (maxy+1, maxx)

    minute = 0
    while True:
        minute += 1
        for i in range(len(blizzardPositions)):
            y, x = blizzardPositions.pop(0)
            direction = blizzardDirections.pop(0)
            if direction == "^":
                y = y-1
                if y == 0:
                    y = maxy
                blizzardPositions.append((y, x))
                blizzardDirections.append(direction)
            if direction == "v":
                y = y+1
                if y == maxy+1:
                    y = 1
                blizzardPositions.append((y, x))
                blizzardDirections.append(direction)
            if direction == "<":
                x = x-1
                if x == 0:
                    x = maxx
                blizzardPositions.append((y, x))
                blizzardDirections.append(direction)
            if direction == ">":
                x = x+1
                if x == maxx+1:
                    x = 1
                blizzardPositions.append((y, x))
                blizzardDirections.append(direction)

        for i in range(len(positions)):
            y, x = positions.pop(0)
            for p1 in [
                (y-1, x),
                (y, x-1),
                (y, x),
                (y, x+1),
                (y+1, x),
            ]:
                if p1 == goal:
                    return minute
                elif (
                    p1 not in blizzardPositions and
                    p1 not in grid and
                    ((p1[0] > 0 and p1[1] > 0) or (p1 == start)) and
                    ((p1[0] <= maxy and p1[1] <= maxx)) and
                    p1 not in positions
                ):
                    positions.append(p1)

        # drawMap(blizzardPositions, blizzardDirections, positions, maxx, maxy)
        print(minute, len(positions), end="\r")


def solve_b(data):
    grid = {}
    blizzardPositions = []
    blizzardDirections = []
    start = (0, 1)
    positions = [start]

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                # wall
                grid[(y, x)] = "#"
            if c in (">", "<", "v", "^"):
                # blizzard
                blizzardPositions.append((y, x))
                blizzardDirections.append(c)

    minx = min(x for (y, x) in grid) + 1
    miny = min(y for (y, x) in grid) + 1
    maxx = max(x for (y, x) in grid) - 1
    maxy = max(y for (y, x) in grid) - 1

    goal = (maxy+1, maxx)

    minute = 0
    for trip in range(3):
        while True:
            minute += 1
            for i in range(len(blizzardPositions)):
                y, x = blizzardPositions.pop(0)
                direction = blizzardDirections.pop(0)
                if direction == "^":
                    y = y-1
                    if y == 0:
                        y = maxy
                    blizzardPositions.append((y, x))
                    blizzardDirections.append(direction)
                if direction == "v":
                    y = y+1
                    if y == maxy+1:
                        y = 1
                    blizzardPositions.append((y, x))
                    blizzardDirections.append(direction)
                if direction == "<":
                    x = x-1
                    if x == 0:
                        x = maxx
                    blizzardPositions.append((y, x))
                    blizzardDirections.append(direction)
                if direction == ">":
                    x = x+1
                    if x == maxx+1:
                        x = 1
                    blizzardPositions.append((y, x))
                    blizzardDirections.append(direction)

            tripFinished = False
            for i in range(len(positions)):
                y, x = positions.pop(0)
                for p1 in [
                    (y-1, x),
                    (y, x-1),
                    (y, x),
                    (y, x+1),
                    (y+1, x),
                ]:
                    if p1 == goal:
                        goal, start = start, goal
                        positions = [p1]
                        print(f"trip {trip} finished after minute", minute)
                        tripFinished = True
                        break
                    elif (
                        p1 not in blizzardPositions and
                        p1 not in grid and
                        ((p1[0] > 0 and p1[1] > 0) or (p1 == start) or (p1 == goal)) and
                        ((p1[0] <= maxy and p1[1] <= maxx) or (p1 == goal) or (p1 == start)) and
                        p1 not in positions
                    ):
                        positions.append(p1)
            if tripFinished:
                break

            # drawMap(blizzardPositions, blizzardDirections, positions, maxx, maxy)
            print(minute, len(positions), end="\r")
    return minute


if __name__ == "__main__":
    main()
