from constants import NUMBER_EMOJIS


class GridSquare:
    FLAG = " 🚩"
    BOMB = " 💣"

    def __init__(self):
        self.has_mine = False
        self.is_cleared = False
        self.is_flagged = False
        self.danger_level = 0

    def draw(self, game_status: int):
        if game_status == 0:
            if self.is_flagged:
                return GridSquare.FLAG
            elif self.is_cleared:
                return f" {NUMBER_EMOJIS[self.danger_level]} "
            else:
                return " · "
        else:
            if self.has_mine:
                return GridSquare.BOMB if game_status == -1 else GridSquare.FLAG
            else:
                return f" {NUMBER_EMOJIS[self.danger_level]} "


