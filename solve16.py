import sys
from aocd import submit, get_data


def main():
    day = 16
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""": 1651,
    }
    test_data_b = {
"""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""": 1707,
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
        for neighbour in grid[current]:
            tentativeGScore = gScore[current] + 1
            if (neighbour not in gScore) or (tentativeGScore < gScore[neighbour]):
                cameFrom[neighbour] = current
                gScore[neighbour] = tentativeGScore
                fScore[neighbour] = tentativeGScore
                openSet.add(neighbour)
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
    rates = {}
    moves = {}
    moveTo = {}
    minutes = 30

    for line in data.splitlines():
        sline = line.split()
        v = sline[1]
        r = int(sline[4][5:-1])
        m = [t.replace(",", "") for t in sline[9:]]

        rates[v] = r
        moves[v] = m

    for k in rates:
        moveTo[k] = {}
        for o, v in rates.items():
            if v:
                moveTo[k][o] = aStar(moves, k, o)[0][1:]

    # position, active valves, remaining minutes, current score
    start = ("AA", tuple(), minutes, 0)
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0

    while openSet:
        current = max(openSet, key=lambda a: fScore.get(a, 0))
        openSet.remove(current)
        if current[2] <= 0:
            continue
        for neighbour in getNeighbours(current, moveTo, rates):
            tentativeGScore = neighbour[-1]
            if (neighbour not in gScore) or (tentativeGScore > gScore[neighbour]):
                cameFrom[neighbour] = current
                gScore[neighbour] = tentativeGScore
                fScore[neighbour] = tentativeGScore
                openSet.add(neighbour)
    best = max((k for k in fScore), key=lambda k: fScore[k])
    return fScore[best]


def getNeighbours(current, moveTo, rates):
    neighbours = []
    position, active, minutes, score = current
    for k, path in moveTo[position].items():
        if k not in active and len(path) <= minutes:
            newMinutes = minutes - len(path) - 1
            newScore = (score + rates[k] * newMinutes)
            neighbours.append((k, active + (k,), newMinutes, newScore))
    return neighbours


def getNeighboursDouble(current, moveTo, valves, minutes):
    neighbours = []
    score, (p0, p1), (m0, m1), active, minute, restScore = current

    # all valves open -> end
    if len(active) == len(valves):
        return [(
            score,
            (p0, p1),
            (m0, m1),
            active,
            minutes,
            restScore,
        )]

    # both need new target
    if minute == m0 == m1:
        for np0 in valves:
            if np0 in active:
                continue
            nm0 = minute + moveTo[p0][np0]
            if nm0 > minutes:
                continue
            for np1 in valves:
                if np1 in active or np1 == np0:
                    continue
                nm1 = minute + moveTo[p1][np1]
                if nm1 > minutes:
                    continue
                newScore = score + valves[np0] * (minutes - nm0) + valves[np1] * (minutes - nm1)
                restScore = getRestScore(valves, active + (np0, np1), minutes - min(nm0, nm1))
                neighbours.append((
                    newScore,
                    (np0, np1),
                    (nm0, nm1),
                    active + (np0, np1),
                    min(nm0, nm1),
                    restScore,
                ))
    elif minute == m0:
        for np0 in valves:
            if np0 in active:
                continue
            nm0 = minute + moveTo[p0][np0]
            if nm0 > minutes:
                continue
            newScore = score + valves[np0] * (minutes - nm0)
            restScore = getRestScore(valves, active + (np0,), minutes - min(nm0, m1))
            neighbours.append((
                newScore,
                (np0, p1),
                (nm0, m1),
                active + (np0,),
                min(nm0, m1),
                restScore,
            ))
    elif minute == m1:
        for np1 in valves:
            if np1 in active:
                continue
            nm1 = minute + moveTo[p1][np1]
            if nm1 > minutes:
                continue
            newScore = score + valves[np1] * (minutes - nm1)
            restScore = getRestScore(valves, active + (np1,), minutes - min(m0, nm1))
            neighbours.append((
                newScore,
                (p0, np1),
                (m0, nm1),
                active + (np1,),
                min(m0, nm1),
                restScore,
            ))
    if not neighbours:
        return [(
            score,
            (p0, p1),
            (m0, m1),
            active,
            minutes,
            restScore,
        )]
    return neighbours


def getRestScore(valves, active, minutes):
    return sum(v for k, v in valves.items() if k not in active) * minutes


def solve_b(data):
    rates = {}
    moves = {}
    moveTo = {}
    minutes = 26

    for line in data.splitlines():
        sline = line.split()
        v = sline[1]
        r = int(sline[4][5:-1])
        m = [t.replace(",", "") for t in sline[9:]]

        rates[v] = r
        moves[v] = m

    for k in rates:
        moveTo[k] = {}
        for o, v in rates.items():
            moveTo[k][o] = len(aStar(moves, k, o)[0][1:]) + 1

    valves = {k: v for k, v in rates.items() if v}

    # current score, positions, arrival minutes, active valves, minute, restScore
    start = (0, ("AA", "AA"), (0, 0), tuple(), 0, getRestScore(valves, tuple(), minutes))
    openSet = [start]
    done = set()
    dropped = 0
    best = 0

    i = 0
    while openSet:
        i += 1
        # score, positions, arrival minutes, active, minute, restScore
        current = openSet.pop()
        score, (p0, p1), (m0, m1), active, minute, restScore = current
        if score + restScore < best:
            dropped += 1
            continue
        if minute >= minutes:
            if score > best:
                print(score, active, " "*50)
                best = score
            continue
        for neighbour in getNeighboursDouble(current, moveTo, valves, minutes):
            if (neighbour not in done):
                done.add(neighbour)
                openSet.append(neighbour)
    return best


if __name__ == "__main__":
    main()
