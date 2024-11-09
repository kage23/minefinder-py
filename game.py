from grid_square import GridSquare
from utils import (
    clear_screen,
    generate_mine,
    get_neighbors,
)

class Game:
    ACTIONS = ["c", "f"] # , "m"] # Clear, Flag, and Mark

    def __init__(self, width:int=10, height:int=10, mines_amount:int=10):
        if width < 5:
            raise ValueError("C'mon! Let's have more width than that :P")
        if width > 99:
            raise ValueError("That's too big!! :P")
        self.width = width
        if height < 5:
            raise ValueError("C'mon! Let's have more height than that :P")
        if height > 99:
            raise ValueError("That's too big!! :P")
        self.height = height
        if mines_amount > (self.width * self.height) - 1:
            raise ValueError("That's too many mines!")
        if mines_amount < 1:
            raise ValueError("C'mon, at least one mine!")
        self.mines_amount = mines_amount
        self.field = self._generate_field()
        self.status = 0 # 0 = active, -1 = lost, 1 = won

    def __str__(self):
        flags_count = len(list(filter(lambda gs: gs.is_flagged, self.field.values())))
        rendered_field = f"\n Mines: {self.mines_amount - flags_count}\n\n"
        rendered_field += self._get_column_numbers_to_print()
        for y in range(self.height):
            if y < 9:
                rendered_field += f" {y + 1}  "
            else:
                rendered_field += f"{y + 1}  "
            for x in range(self.width):
                grid_square = self.field[f"{x},{y}"]
                rendered_field += grid_square.draw(self.status)
            rendered_field += "\n"
        return rendered_field

    def _get_column_numbers_to_print(self):
        field = "    "
        for i in range(self.width):
            if i < 9:
                field += f" {str(i + 1)} "
            else:
                field += f" {str(i + 1)}"
        field += "\n\n"
        return field

    def _generate_field(self):
        # Create grid squares
        field: dict[str, GridSquare] = {}
        for x in range(self.width):
            for y in range(self.height):
                field[f"{x},{y}"] = GridSquare()

        # Set mines
        mine_list = set[str]()
        while len(mine_list) < self.mines_amount:
            mine_list.add(generate_mine(self.width, self.height))
        for mine in mine_list:
            field[mine].has_mine = True

        # Set danger levels
        for point, grid_square in field.items():
            if grid_square.has_mine:
                grid_square.danger_level = 9
            else:
              neighbors = get_neighbors(point, self.width, self.height)
              grid_square.danger_level = len(list(filter(lambda n: field[n].has_mine, neighbors)))

        return field

    def _gameplay_loop(self):
        clear_screen()
        print(self)
        point = self._get_point()
        action = self._get_action(point)
        self._take_action(action, point)
        self._evaluate_status()

    def _get_point(self) -> str:
        while True:
            row = self._get_row()
            col = self._get_col()
            point = f"{col},{row}"
            if self.field[point].is_cleared:
                print("That square has already been cleared!")
            else:
                return point

    def _get_row(self) -> int:
        while True:
            try:
                row = int(input("Select a row: ").strip()) - 1
                if 0 <= row < self.height:
                    return row
            except ValueError:
                continue

    def _get_col(self) -> int:
        while True:
            try:
                col = int(input("Select a column: ").strip()) - 1
                if 0 <= col < self.height:
                    return col
            except ValueError:
                continue

    def _get_action(self, point:str) -> str | None:
        while True:
            # action = input("Select (C)lear, (F)lag/unflag, or (M)ark: ").strip().lower()
            action = input("Select (C)lear or (F)lag/unflag: ").strip().lower()
            if action not in Game.ACTIONS:
                print("Invalid action!")
            if self.field[point].is_cleared:
                print("That square is already cleared!")
            if action == "c" and self.field[point].is_flagged:
                input("You can't clear a flagged square!")
                return None
            else:
                return action

    def _take_action(self, action: str | None, point: str) -> None:
        match action:
            case "c":
                self._recursively_clear(point)
            case "f":
                self._flag(point)
            case _:
                pass

    def _recursively_clear(self, point:str) -> None:
        self.field[point].is_cleared = True
        if self.field[point].danger_level == 0:
            for neighbor in get_neighbors(point, self.width, self.height):
                if not self.field[neighbor].is_cleared and not self.field[neighbor].is_flagged:
                    self._recursively_clear(neighbor)

    def _flag(self, point:str) -> None:
        self.field[point].is_flagged = not self.field[point].is_flagged

    def _evaluate_status(self) -> None:
        mines = list(filter(lambda gs: gs.has_mine, self.field.values()))

        # Check for losing condition
        for mine in mines:
            if mine.is_cleared:
                self.status = -1

        # Check for winning condition
        if self.status != -1:
            size = self.width * self.height
            cleared_count = len(list(
                filter(lambda gs: gs.is_cleared, self.field.values())
            ))
            if cleared_count + self.mines_amount == size:
                self.status = 1

