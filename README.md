# MINEFINDER
#### Video Demo: https://youtu.be/CDIbYu6bWvA
#### Description: A clone of the game Minesweeper

Clone this repo and then run `python minefinder.py` to play.

You are presented with a field and tasked with discovering all of the mines in the field.
Select a grid square, enter its row and column, and then select whether you would like to Flag or Clear that square.
Flagging a square indicates that you believe that there is a mine on that square.
Clearing a square indicates you believe there is no mine on that square.
When you clear a square, the cleared square will indicate how many adjacent squares contain a mine.
If a cleared square has no adjacent mines, all adjacent squares are also cleared, and the same rule applies to them.
If you attempt to clear a square that contains a mine, you lose.
If you clear all squares that do not contain a mine, you win.
You don't actually have to flag mine-containing squares to win, just clear all non-mine-containing squares.


#### Technical Breakdown

The project consists of the following files:

- `minefinder.py` is the main file of the project. It runs the game via the `main` function.
- `game.py` contains the GridSquare and Game classes.
- `constants.py` contains constants for the project.
- `utils.py` contains a few utility functions used by the project.
  - `generate_mine` function.
  - `get_neighbors` function.
  - `clear_screen` function.

##### class `GridSquare`

This is the representation of a single space in the game field.

- `GridSquare.__init__` intializes it and sets default state values.
- `GridSquare.__str__` prints it depending on its state.

##### class `Game`

This is the representation of the game.

- `Game.__init__` initializes the game.
  - Accepts `width:int`, `height:int`, and `mines_amount:int` parameters. All three default to `10`.
  - `width`, `height`, and `mines_amount` are all set as properties of the `Game`, after performing some validation.
  - The game's `field` property gets set via the `_generate_field` method.
    - The `field` initially does not have any mines in it.
  - A `_mines_set` boolean parameter is initialized as `False` in the game.
  - The game's `status` is initialized as active (`0`).
- `Game.__str__` creates a string representation of the game, to be printed to the screen.
  - First, it prints the number of mines remaining (calculated as total number of mines, minus number of flags the player has placed).
  - Then, it generates the column numbers to print along the top of the game.
  - Finally, it generates the individual rows to be printed by accessing the `__str__` method of the grid squares in the field.
- `Game._get_column_numbers_to_print` does what the name of the function says it does. Used by `Game.__str__`.
- `Game._generate_field` creates the game field.
  - It creates a grid square for every xy coordinate of the field, and sets them in a dict.
- `Game._set_mines` adds mines to the game field.
  - It accepts a `safe_point` str parameter representing the point that the player would like to clear.
  - Using the game's `mines_amount` parameter, it generates a list of squares to be mined, ensuring that the passed safe point is not in the list, then sets the `has_mine` property on the appropriate grid squares in the game's `field` to `True`.
  - It updates the game's `_mines_set` parameter to `True`.
  - It calls the `_generate_danger_levels` function.
- `Game._generate_danger_levels` calculates and sets danger levels for every grid square.
  - It retrieves a list of neighbors of each square, and then counts how many of those neighbors have a mine, then sets the result as the square's danger level.
  - If the square itself has a mine, its danger level is set to 9.
- `Game._gameplay_loop` is what the name on the tin says it is - the gameplay loop.
  - It clears the screen and prints the current game status, receives and applies the player's next move, and then evaluates the game's status.
- `Game._get_point` handles receiving player input for the grid square they would like to select.
  - It validates the player's selection - they cannot select a square that has already been cleared.
- `Game._get_row` handles receiving player input for the row of the grid square they would like to select.
  - It validates the player's selection against the height of the field.
- `Game._get_col` handles receiving player input for the column of the grid square they would like to select.
  - It validates the player's selection against the width of the field.
- `Game._get_action` handles receiving player input for the action they would like to take.
  - It accepts their selected grid square as a parameter.
  - It validates their action selection to ensure that it's a valid action that can be taken on the selected square.
- `Game._take_action` handles applying the player's action.
  - It accepts the player's selected action and grid square as parameters.
  - If the player selected the `clear` action, and the game's `_mines_set` parameter is `False`, the `_set_mines` function is called, with the player's selected point passed in as the safe point.
  - It calls either the `Game._recursively_clear` or `Game._flag` function, depending on the selected action.
- `Game._recursively_clear` handles clearing the selected square, as well as any other squares that should be cleared from this action.
  - It sets the `is_cleared` property of the selected square to `True`.
  - If the selected square has a danger level of `0`, it gets all adjacent neighbors of the square, and for each neighbor, if it's not already either cleared or flagged, recursively calls the `Game._recursively_clear` function on the neighbor.
- `Game._flag` toggles the `is_flagged` status of the grid square at the given point.
- `Game._evaluate_status` determines and sets the game's status. `-1` means the game has been lost, `0` means the game is active, and `1` means the game has been won.
  - If any mine has been cleared, the game has been lost.
  - Otherwise, if the number of cleared squares plus the number of mines equals the size of the field, the game has been won.

##### `generate_mine`

This accepts `width:int` and `height:int` parameters, and returns a string in the form of `f"{x},{y}"` within the field indicated by the `width` and `height` parameters.

##### `get_neighbors`

This accepts `point:str`, `width:int`, and `height:int` parameters, and returns a `list` of `f"{x},{y}"` strings representing points that are adjacent to the given point, and within the field indicated by the `width` and `height` parameters.

##### `clear_screen`

This accepts no parameters, and returns `None`. As a side effect, it clears the terminal. It was taken from `https://www.geeksforgeeks.org/clear-screen-python/`.

##### `main`

This accepts no parameters, and returns `None`. It initializes the game, runs the gameplay loop until the game is over, and prints the final result.

#### TODO:
##### Sooner:
- implement "first clear is always safe" feature!!!
- implement Mark feature
- allow player to set game parameters
  - CLI params
  - In-app prompts if CLI params not provided

##### Later:
- replace most of this README documentation with docstrings in the actual code
- implement "difficulty levels" instead of (or supplementing) direct setting of game parameters
- implement a GUI - maybe [Pyxel](https://github.com/kitao/pyxel)?
- implement some sort of persisting win/loss record
- implement a timer
- implement a high scores list
