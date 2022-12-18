from aocd import submit, get_data
import logging

logging.basicConfig(filename="./debug.log", filemode="w", level=999)


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
    moves = ""

    def __init__(self, data, target):
        self.height = 0
        self.cave = {}
        self.jetpos = 0
        self.rockpos = 0
        self.i = 0
        self.jets = [1 if c == ">" else -1 for c in data]

        while self.i < 2023:
            self.step()

    def step(self):
        if not self.rock:
            self.i += 1
            self.rock = self.rocks[self.rockpos]
            self.rockpos = (self.rockpos + 1) % len(self.rocks)
            self.width = len(self.rock[0])
            self.bot = self.height + 3
            self.left = 2
            self.right = self.left + self.width
            self.new = {}
            self.newcounter = 0
            self.moves = ""
            print(self.i, self.height, end="\r")

        self.jet = self.jets[self.jetpos]
        self.jetpos = (self.jetpos + 1) % len(self.jets)
        self.moves += ">" if self.jet == 1 else "<"

        # horizontal movement (by jet)
        if self.left + self.jet >= 0 and self.right + self.jet <= 7:
            if not self.checkCollision(hor=self.jet):
                self.left += self.jet
                self.right += self.jet

        # vertical movement (downwards)
        if self.checkCollision(vert=1):
            self.addRock()
            # self.debug()
            self.filedebug()

        self.bot -= 1
        if self.rock:
            for y, l in enumerate(reversed(self.rock)):
                for x, c in enumerate(l):
                    if c == "#":
                        self.new[(y+self.bot, x+self.left)] = self.newcounter

        # if self.i >= 11:
        self.newcounter += 1

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
        # self.debug()

    def debug(self):
        i = 0
        print()

        for y in range(self.height+5, -1, -1):
            i += 1
            print("|", end="")
            for x in range(7):
                if (y, x) in self.cave:
                    print("#", end="")
                elif (y, x) in self.new:
                    print(str(self.new[(y, x)])[-1], end="")
                else:
                    print(".", end="")
            print("|  |", end="")
            for x in range(7):
                if (y, x) in self.cave:
                    print(self.cave[(y, x)], end="")
                else:
                    print(".", end="")
            print("|")
            if i > 20:
                input("Press enter")
                return
        print("-"*9, "", "-"*9)
        # print(self.bot, self.left, self.right)
        input("Press enter")

    def filedebug(self):
        logging.warning("")
        logging.warning("----------------------")
        logging.warning(f"I: {self.i}")
        logging.warning(self.moves)
        ll = ""

        for y in range(self.height+5, -1, -1):
            ll += "|"
            for x in range(7):
                if (y, x) in self.cave:
                    ll += str(self.cave[(y, x)])
                else:
                    ll += "."
            ll += "|"
            logging.warning(ll)
            ll = ""
        logging.warning("-"*9)


def solve_a(data):
    g = Game(data, target=2023)
    return g.height


def solve_b(data):
    g = Game(data, target=1_000_000_000_000)
    return g.height


if __name__ == "__main__":
    main()
