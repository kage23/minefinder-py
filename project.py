import os
import random
from typing import Tuple

type Point = Tuple[int, int]

NUMBER_EMOJIS = [" ", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

class Game:
    ACTIONS = ["c", "f"] # , "m"] # Clear, Flag, and Mark

    def __init__(self, width:int=10, height:int=10, mines_amount:int=10):
        self.width = width
        self.height = height
        self.mines = mines_amount
        self._danger_levels = self.generate_danger_levels()
        self.flags = set[Tuple[int, int]]()
        # self.marks = set[Tuple[int, int]]()
        self.cleared = set[Tuple[int, int]]()
        self.status = 0 # 0 = active, -1 = lost, 1 = won

    def __str__(self):
        field = f"\n Mines: {len(self.mines) - len(self.flags)}\n\n"
        field += self.get_column_numbers_to_print()
        field += self.generate_rows_to_print()
        return field

    def get_column_numbers_to_print(self):
        field = "    "
        for i in range(self.width):
            if i < 9:
                field += f" {str(i + 1)} "
            else:
                field += f" {str(i + 1)}"
        field += "\n\n"
        return field

    def generate_rows_to_print(self):
        field = ""
        for y in range(self.height):
            if y < 9:
                field += f" {y + 1}  "
            else:
                field += f"{y + 1}  "
            for x in range(self.width):
                if (x, y) in self.flags or (self.status == 1 and (x, y) in self.mines):
                    field += " 🚩"
                elif (x, y) in self.cleared:
                    if (x, y) in self.mines:
                        field += " 💣"
                    else:
                        field += f" {NUMBER_EMOJIS[self._danger_levels[(x, y)]]} "
                # elif (x, y) in self.marks:
                #     field += " ❓"
                else:
                    field += " · "
            field += "\n"
        return field

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width:int):
        if width < 5:
            raise ValueError("C'mon! Let's have more width than that :P")
        if width > 99:
            raise ValueError("That's too big!! :P")
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height:int):
        if height < 5:
            raise ValueError("C'mon! Let's have more height than that :P")
        if height > 99:
            raise ValueError("That's too big!! :P")
        self._height = height

    @property
    def mines(self):
        return self._mines

    @mines.setter
    def mines(self, mines_amount:int):
        if mines_amount > (self.width * self.height) - 1:
            raise ValueError("That's too many mines!")
        mine_list = set[Point]()
        while len(mine_list) < mines_amount:
            mine_list.add(generate_mine(self.width, self.height))
        self._mines = mine_list

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status:int):
        if status not in [-1, 0, 1]:
            raise ValueError("invalid status")
        self._status = status

    def generate_danger_levels(self):
        danger_levels = {}
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.mines:
                    danger_levels[(x, y)] = 9
                else:
                    danger_levels[(x, y)] = count_neighboring_mines((x, y), self)
        return danger_levels

    def gameplay_loop(self):
        clear_screen()
        print(self)
        point = self.get_point()
        action = self.get_action(point)
        self.take_action(action, point)
        self.evaluate_status()

    def get_point(self) -> Point:
        while True:
            row = self.get_row()
            col = self.get_col()
            point = (col, row)
            if point in self.cleared:
                print("That square has already been cleared!")
            else:
                return point

    def get_row(self) -> int:
        while True:
            try:
                row = int(input("Select a row: ").strip()) - 1
                if 0 <= row < self.height:
                    return row
            except ValueError:
                continue

    def get_col(self) -> int:
        while True:
            try:
                col = int(input("Select a column: ").strip()) - 1
                if 0 <= col < self.height:
                    return col
            except ValueError:
                continue

    def get_action(self, point:Point):
        while True:
            # action = input("Select (C)lear, (F)lag, or (M)ark: ").strip().lower()
            action = input("Select (C)lear or (F)lag/unflag: ").strip().lower()
            if action not in Game.ACTIONS:
                print("Invalid action!")
            if point in self.cleared:
                print("That square is already cleared!")
            if action == "c" and point in self.flags:
                input("You can't clear a flagged square!")
                return None
            else:
                return action

    def take_action(self, action, point:Point):
        if action != None:
            match action:
                case "c":
                    self.recursively_clear(point)
                case "f":
                    self.flag(point)

    def recursively_clear(self, point:Point):
        self.cleared.add(point)
        if self._danger_levels[point] == 0:
            for neighbor in get_neighbors(point, self.width, self.height):
                if neighbor not in self.cleared and neighbor not in self.flags:
                    self.recursively_clear(neighbor)

    def flag(self, point:Point):
        if point in self.flags:
            self.flags.remove(point)
        else:
            self.flags.add(point)

    def evaluate_status(self):
        for mine in self.mines:
            if mine in self.cleared:
                self.status = -1
        if self.status != -1:
            size = self.width * self.height
            if len(self.cleared) + len(self.mines) == size:
                self.status = 1


def generate_mine(width:int, height:int) -> Point:
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    return (x, y)


def get_neighbors(point:Point, width:int, height:int) -> list[Point]:
    x, y = point
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0), # 4-way
        (1, 1), (1, -1), (-1, 1), (-1, -1) # Diagonals
    ]
    return list(filter(
        lambda n: 0 <= n[0] < width and 0 <= n[1] < height,
        map(lambda d: (x + d[0], y + d[1]), directions)
    ))


def count_neighboring_mines(point:Point, game:Game) -> int:
    neighbors = get_neighbors(point, game.width, game.height)
    return len(list(filter(lambda p: p in game.mines, neighbors)))


def clear_screen():
    """
    Clear the terminal. This was taken from https://www.geeksforgeeks.org/clear-screen-python/.
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For macOS and Linux
    else:
        os.system("clear")


def main():
    game = Game(10, 10, 5)
    while game.status == 0:
        game.gameplay_loop()
    clear_screen()
    print(game)
    print("You win" if game.status == 1 else "You lose")


if __name__ == "__main__":
    main()
