import sys
from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 12
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""": 31,
    }
    test_data_b = {
        """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""": 29,
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


def aStar(grid, start, goal):
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))

        openSet.remove(current)
        for neighbor in grid[current]["moves"]:
            tentativeGScore = gScore[current] + 1
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)
    if goal in fScore:
        return (reconstructPath(cameFrom, goal), fScore[goal])
    return ([], sys.maxsize)


def reconstructPath(cameFrom, current):
    path = [current]
    pathSum = 0
    while current in cameFrom.keys():
        current = cameFrom[current]
        pathSum += 1
        path = [current] + path
    return path


def solve_a(data):
    grid = {}
    goal = None
    start = None
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "E":
                goal = (y, x)
                grid[(y, x)] = {"ele": alphabet.index("z")}
            elif c == "S":
                start = (y, x)
                grid[(y, x)] = {"ele": alphabet.index("a")}
            else:
                grid[(y, x)] = {"ele": alphabet.index(c)}

    maxy = max(y for (y, _) in grid)
    maxx = max(x for (_, x) in grid)

    for y in range(maxy + 1):
        for x in range(maxx + 1):
            grid[(y, x)]["moves"] = []
            for other in [(y-1, x), (y, x-1), (y, x+1), (y+1, x)]:
                if other[0] < 0 or other[0] > maxy or other[1] < 0 or other[1] > maxx:
                    continue
                if grid[other]["ele"] <= grid[(y, x)]["ele"] + 1:
                    grid[(y, x)]["moves"].append(other)

    return aStar(grid, start, goal)[1]


def solve_b(data):
    grid = {}
    goal = None
    starts = None
    stars = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "E":
                goal = (y, x)
                grid[(y, x)] = {"ele": alphabet.index("z")}
            elif c == "S":
                grid[(y, x)] = {"ele": alphabet.index("a")}
            else:
                grid[(y, x)] = {"ele": alphabet.index(c)}

    maxy = max(y for (y, _) in grid)
    maxx = max(x for (_, x) in grid)

    for y in range(maxy + 1):
        for x in range(maxx + 1):
            grid[(y, x)]["moves"] = []
            for other in [(y-1, x), (y, x-1), (y, x+1), (y+1, x)]:
                if other[0] < 0 or other[0] > maxy or other[1] < 0 or other[1] > maxx:
                    continue
                if grid[other]["ele"] <= grid[(y, x)]["ele"] + 1:
                    grid[(y, x)]["moves"].append(other)

    starts = [k for (k, v) in grid.items() if v["ele"] == 0]
    for start in starts:
        stars[start] = aStar(grid, start, goal)[1]

    return min(stars.values())


if __name__ == "__main__":
    main()
