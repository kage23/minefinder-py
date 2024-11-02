from typing import Tuple

from constants import NUMBER_EMOJIS
from game_types import Point
from utils import (
    clear_screen,
    generate_mine,
    get_neighbors,
)

class GridSquare:
    FLAG = " 🚩"
    BOMB = " 💣"

    def __init__(self):
        self.has_mine = False
        self.is_cleared = False
        self.is_flagged = False
        self.danger_level = 0
        self.game_status = 0

    def __str__(self):
        if self.game_status == 0:
            if self.is_flagged:
                return GridSquare.FLAG
            elif self.is_cleared:
                return f" {NUMBER_EMOJIS[self.danger_level]} "
            else:
                return " · "
        else:
            if self.has_mine:
                return GridSquare.BOMB if self.game_status == -1 else GridSquare.FLAG
            else:
                return f" {NUMBER_EMOJIS[self.danger_level]} "


class Game:
    ACTIONS = ["c", "f"] # , "m"] # Clear, Flag, and Mark

    def __init__(self, width:int=10, height:int=10, mines_amount:int=10):
        self.width = width
        self.height = height
        self.field = (width, height, mines_amount)
        self.mines = mines_amount
        self._danger_levels = self.generate_danger_levels()
        self.flags = set[Point]()
        # self.marks = set[Point]()
        self.cleared = set[Point]()
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
    def field(self):
        return self._field

    @field.setter
    def field(self, params: Tuple[int, int, int]):
        width, height, mines_amount = params

        if mines_amount > (width * height) - 1:
            raise ValueError("That's too many mines!")
        if mines_amount < 1:
            raise ValueError("C'mon, at least one mine!")

        field: dict[Point, GridSquare] = {}
        for x in range(width):
            for y in range(height):
                field[(x, y)] = GridSquare()

        mine_list = set[Point]()
        while len(mine_list) < mines_amount:
            mine_list.add(generate_mine(self.width, self.height))
        for mine in mine_list:
            x, y = mine
            field[(x, y)].has_mine = True

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
                    danger_levels[(x, y)] = self.count_neighboring_mines((x, y))
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

    def count_neighboring_mines(self, point:Point) -> int:
      neighbors = get_neighbors(point, self.width, self.height)
      return len(list(filter(lambda p: p in self.mines, neighbors)))

