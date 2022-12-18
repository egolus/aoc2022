from aocd import submit, get_data


def main():
    day = 17
    year = 2022
    data = get_data(day=day, year=year)

    test_data_a = {
        ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>": 3068,
    }
    test_data_b = {
        ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>": 1_514_285_714_288,
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


class Game():
    jetpos = None
    jets = None
    rockpos = None
    rocks = [
        ["####"],
        [" # ",
         "###",
         " # "],
        ["###",
         "  #",
         "  #"],
        ["#",
         "#",
         "#",
         "#"],
        ["##",
         "##"],
    ]
    rock = None
    cave = None
    new = None
    newcounter = None
    height = None
    i = None
    positions = None

    def __init__(self, data, target):
        self.height = 0
        self.cave = {}
        self.jetpos = 0
        self.rockpos = 0
        self.i = 0
        self.jets = [1 if c == ">" else -1 for c in data]
        self.positions = set()

        first = None
        second = None
        done = False
        heightadded = 0
        while self.i < target:
            self.step()
            if not done and self.rock is None and (self.jetpos, self.rockpos) in self.positions:
                if not first:
                    first = (self.i, self.height, self.jetpos, self.rockpos)
                elif not second:
                    second = (self.i, self.height, self.jetpos, self.rockpos)
                elif self.jetpos == second[2] and self.rockpos == second[3]:
                    loop = self.i - second[0]
                    times = (target-self.i) // loop
                    heightadded = (self.height-second[1]) * times
                    self.i += (self.i-second[0]) * times
                    done = True
            self.positions.add((self.jetpos, self.rockpos))
        self.height += heightadded

    def step(self):
        if not self.rock:
            self.i += 1
            self.rock = self.rocks[self.rockpos]
            self.rockpos = (self.rockpos + 1) % len(self.rocks)
            self.width = len(self.rock[0])
            self.bot = self.height + 3
            self.left = 2
            self.right = self.left + self.width

        self.jet = self.jets[self.jetpos]
        self.jetpos = (self.jetpos + 1) % len(self.jets)

        # horizontal movement (by jet)
        if self.left + self.jet >= 0 and self.right + self.jet <= 7:
            if not self.checkCollision(hor=self.jet):
                self.left += self.jet
                self.right += self.jet

        # vertical movement (downwards)
        if self.checkCollision(vert=1):
            self.addRock()

        self.bot -= 1

    def checkCollision(self, hor=0, vert=0):
        if self.bot-vert <= -1:
            return True
        for y in range(len(self.rock)):
            for x in range(self.width):
                if (self.rock[y][x] == "#" and
                        (self.bot+y-vert, self.left+x+hor) in self.cave):
                    return True

    def addRock(self):
        for y, l in enumerate(self.rock):
            for x, c in enumerate(l):
                if c == "#":
                    self.cave[(y+self.bot, x+self.left)] = self.rockpos
        self.height = max(y for (y, _) in self.cave) + 1
        self.rock = None


def solve_a(data):
    g = Game(data, target=2023)
    return g.height


def solve_b(data):
    g = Game(data, target=1_000_000_000_001)
    return g.height


if __name__ == "__main__":
    main()
