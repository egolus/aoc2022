import math
import concurrent.futures
from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 19
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
"""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""": 33,
    }
    test_data_b = {
"""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""": 62,
    }

    # for i, (test, true) in enumerate(test_data_a.items()):
        # result = solve_a(test)
        # print(f"result {i}: {result}\n")
        # assert result == true, f"{result} != {true}"

    # result_a = solve_a(data)
    # submit(result_a, part="a", day=day, year=year)

    # for i, (test, true) in enumerate(test_data_b.items()):
        # result = solve_b(test)
        # print(f"result {i}: {result}\n")
        # assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    submit(result_b, part="b", day=day, year=year)


def getNeighbour(state, blueprint, maxMinutes, maxCosts=None):
    """
    Return a list of nodes that can be directly reached from the current
    node.
    """
    order = ["ore", "clay", "obsidian", "geode"]
    neighbours = []
    minute, items, robots = state

    # just wait until the end
    available = dict(items)
    bots = {bot: 0 for bot in order}
    for robot in robots:
        available[robot] += maxMinutes - minute
        bots[robot] += 1
    neighbours.append((
        maxMinutes,
        tuple(available.items()),
        robots,
    ))
    for material in order:
        if material in maxCosts and bots[material] >= maxCosts[material]:
            continue
        available = dict(items)
        # can be built directly
        if all(available[cost[1]] >= cost[0] for cost in blueprint[material]):
            minutesNeeded = 1
        # not enough material but there's robots to eventually produce all
        # needed materials
        elif all(cost[1] in robots for cost in blueprint[material]):
            missing = []
            for cost in blueprint[material]:
                if available[cost[1]] < cost[0]:
                    missing.append((cost[0] - available[cost[1]], cost[1]))
            minutesNeeded = max(
                math.ceil(m[0] / len([r for r in robots if r == m[1]]))
                for m in missing
            ) + 1
            # can't be built in time
            if minute + minutesNeeded >= maxMinutes:
                continue
        # can't be built with current robots
        else:
            continue
        for cost in blueprint[material]:
            available[cost[1]] -= cost[0]
        for robot in robots:
            available[robot] += minutesNeeded
        neighbours.append((
            minute + minutesNeeded,
            tuple(available.items()),
            robots + (material,),
        ))
    return neighbours


def getMaxCosts(bprint):
    materials = ["ore", "clay", "obsidian", "geode"]
    maxCosts = {}
    for material in materials:
        for botCosts in bprint.values():
            for v, k in botCosts:
                if k == material:
                    if k not in maxCosts or v > maxCosts[k]:
                        maxCosts[k] = v
    return maxCosts


def runTask(no, bprint, minutes=24):
    # (minutes, stash, robots)
    start = (
        0,
        (("ore", 0), ("clay", 0), ("obsidian", 0), ("geode", 0)),
        ("ore",),
    )
    maxCosts = getMaxCosts(bprint)
    if maxCosts:
        pprint(f"{no}, {maxCosts=}")
    states = [start]
    best = 0
    while states:
        current = states.pop()
        if current[0] >= minutes:
            if current[1][3][1] > best:
                print(no, current)
                best = current[1][3][1]
            continue
        states.extend(getNeighbour(current, bprint, minutes, maxCosts=maxCosts))
    return best


def solve_a(data):
    sol = 0
    bprints = {}
    for i, line in enumerate(data.splitlines()):
        bprint = {}
        sline = line.split()
        bprint["ore"] = ((int(sline[6]), "ore"),)
        bprint["clay"] = ((int(sline[12]), "ore"),)
        bprint["obsidian"] = ((int(sline[18]), "ore"), (int(sline[21]), "clay"))
        bprint["geode"] = ((int(sline[27]), "ore"), (int(sline[30]), "obsidian"))
        bprints[i+1] = bprint

    pprint(bprints)
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(runTask, no, bprint): (no, bprint)
                   for no, bprint in bprints.items()}
        for future in concurrent.futures.as_completed(futures):
            no, bprint = futures[future]
            sol += no * future.result()
        return sol


def solve_b(data):
    sol = 1
    bprints = {}
    for i, line in enumerate(data.splitlines()[:3]):
        bprint = {}
        sline = line.split()
        bprint["ore"] = ((int(sline[6]), "ore"),)
        bprint["clay"] = ((int(sline[12]), "ore"),)
        bprint["obsidian"] = ((int(sline[18]), "ore"), (int(sline[21]), "clay"))
        bprint["geode"] = ((int(sline[27]), "ore"), (int(sline[30]), "obsidian"))
        bprints[i+1] = bprint

    pprint(bprints)
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(runTask, no, bprint, 32): (no, bprint)
                   for no, bprint in bprints.items()}
        for future in concurrent.futures.as_completed(futures):
            no, bprint = futures[future]
            sol *= future.result()
        return sol
    res = 0
    return res


if __name__ == "__main__":
    main()
