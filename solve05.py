from aocd import submit, get_data


def main():
    day = 5
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

 move 1 from 2 to 1
 move 3 from 1 to 3
 move 2 from 2 to 1
 move 1 from 1 to 2""": "CMZ",
    }
    test_data_b = {
        """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

 move 1 from 2 to 1
 move 3 from 1 to 3
 move 2 from 2 to 1
 move 1 from 1 to 2""": "MCD",
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
    stacks = {}
    data = data.split("\n\n")
    stacklines = []
    for line in data[0].splitlines()[:-1]:
        s = []
        for i in range(0, len(line), 4):
            s.append(line[i:i+4])
        stacklines.append(s)
    for stack in range(len(stacklines[0])):
        stacks[stack] = list(reversed([stackline[stack].strip() for stackline in stacklines if stackline[stack].strip()]))

    for line in data[1].splitlines():
        sline = line.split()
        count, _from, _to = int(sline[1]), int(sline[3])-1, int(sline[5])-1
        for i in range(count):
            crate = stacks[_from].pop(-1)
            stacks[_to].append(crate)

    return "".join([stack[-1][1:-1] for stack in stacks.values()])


def solve_b(data):
    stacks = {}
    data = data.split("\n\n")
    stacklines = []
    for line in data[0].splitlines()[:-1]:
        s = []
        for i in range(0, len(line), 4):
            s.append(line[i:i+4])
        stacklines.append(s)
    for stack in range(len(stacklines[0])):
        stacks[stack] = list(reversed([stackline[stack].strip() for stackline in stacklines if stackline[stack].strip()]))

    for line in data[1].splitlines():
        sline = line.split()
        count, _from, _to = int(sline[1]), int(sline[3])-1, int(sline[5])-1
        crates = stacks[_from][-count:]
        stacks[_to].extend(crates)
        stacks[_from][-count:] = []

    return "".join([stack[-1][1:-1] for stack in stacks.values()])


if __name__ == "__main__":
    main()
