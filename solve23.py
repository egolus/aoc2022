from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 23
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""": 110,
    }
    test_data_b = {
"""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""": 20,
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


def drawMap(grid):
    minx = min(x for (y, x) in grid)
    maxx = max(x for (y, x) in grid)
    miny = min(y for (y, x) in grid)
    maxy = max(y for (y, x) in grid)

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (y, x) in grid:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


def solve_a(data):
    grid = {}

    moves = [
        (((-1, -1), (-1, 0), (-1, +1)), (-1, 0)),
        (((+1, -1), (+1, 0), (+1, +1)), (+1, 0)),
        (((-1, -1), (0, -1), (+1, -1)), (0, -1)),
        (((-1, +1), (0, +1), (+1, +1)), (0, +1)),
     ]

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                grid[(y, x)] = c

    # drawMap(grid)

    for round in range(10):
        for elf in grid:
            y, x = elf
            if not any(e in grid for e in (
                (y-1, x-1),
                (y-1, x),
                (y-1, x+1),
                (y, x-1),
                (y, x+1),
                (y+1, x-1),
                (y+1, x),
                (y+1, x+1),
            )):
                grid[elf] = (y, x)
            else:
                for neighbours, move in moves:
                    if not any((y+e[0], x+e[1]) in grid for e in neighbours):
                        grid[elf] = (y+move[0], x+move[1])
                        break
                else:
                    grid[elf] = (y, x)

        nextGrid = {}
        for elf, move in grid.items():
            if len([m for m in grid.values() if m == move]) == 1:
                nextGrid[move] = "#"
            else:
                nextGrid[elf] = "#"

        moves.append(moves.pop(0))
        grid = nextGrid

        # drawMap(grid)

    minx = min(x for (y, x) in grid)
    maxx = max(x for (y, x) in grid)
    miny = min(y for (y, x) in grid)
    maxy = max(y for (y, x) in grid)
    res = 0
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (y, x) not in grid:
                res += 1
    return res


def solve_b(data):
    grid = {}

    moves = [
        (((-1, -1), (-1, 0), (-1, +1)), (-1, 0)),
        (((+1, -1), (+1, 0), (+1, +1)), (+1, 0)),
        (((-1, -1), (0, -1), (+1, -1)), (0, -1)),
        (((-1, +1), (0, +1), (+1, +1)), (0, +1)),
     ]

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                grid[(y, x)] = c

    # drawMap(grid)

    round = 0
    while True:
        round += 1
        print(round, end="\r")
        old = tuple(grid)
        for elf in grid:
            y, x = elf
            if not any(e in grid for e in (
                (y-1, x-1),
                (y-1, x),
                (y-1, x+1),
                (y, x-1),
                (y, x+1),
                (y+1, x-1),
                (y+1, x),
                (y+1, x+1),
            )):
                grid[elf] = (y, x)
            else:
                for neighbours, move in moves:
                    if not any((y+e[0], x+e[1]) in grid for e in neighbours):
                        grid[elf] = (y+move[0], x+move[1])
                        break
                else:
                    grid[elf] = (y, x)

        nextGrid = {}
        for elf, move in grid.items():
            if len([m for m in grid.values() if m == move]) == 1:
                nextGrid[move] = "#"
            else:
                nextGrid[elf] = "#"

        moves.append(moves.pop(0))
        if tuple(nextGrid) == old:
            return round
        grid = nextGrid


if __name__ == "__main__":
    main()
