# MINEFINDER
#### Video Demo:  <URL HERE>
#### Description: A clone of the game Minesweeper

Clone this repo and then run `python project.py` to play.

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

The project consists of one main file, `project.py`, and one test file, `test_project.py`.
`project.py` contains the following:
- `Game` class.
- `generate_mine` function.
- `get_neighbors` function.
- `count_neighboring_mines` function.
- `clear_screen` function.
- `main` function.

With the exception of `clear_screen` and `main`, all of these functions should probably actually be part of the `Game` class.
They were implemented outside of the class due to the following requirements of the
[CS50P Final Project](https://cs50.harvard.edu/python/2022/project/):
> Your project must have a `main` function and three or more additional functions. At least three of those additional functions must be accompanied by tests that can be executed with `pytest`.

> Your 3 required custom functions other than `main` must also be in `project.py` and defined at the same indentation level as `main` (i.e., not nested under any classes or functions).

##### class Game

This is the representation of the game.

- `Game.__init__` initializes the game.
  - Accepts `width:int`, `height:int`, and `mines_amount:int` parameters. All three default to `10`.
  - `width` and `height` are both set as protected properties of the `Game`, after performing some validation.
  - `mines_amount` gets translated to the `Game.mines` property, which is a set of `(x, y)` tuples represting squares that have mines.
    - The `mines` setter accepts the `mines_amount:int` param, validates that it's an acceptable number of mines (ie not more than the field can hold), and then uses the `generate_mine` util function to generate the designated number of mines.
  - After generating mines, every square's "danger level" (number of adjacent mines) is calculated and stored.
    - This could be done on an ad hoc basis as squares are revealed, but it seemed simpler and more efficient to pre-calculate it all.
  - `Game.flags` and `Game.cleared` properties are initialized as empty sets. They will be utilized to store points that the user has flagged, and points that have been cleared, respectively.
  - The game's `status` is initialized as active (`0`).
- `Game.__str__` creates a string representation of the game, to be printed to the screen.
  - First, it prints the number of mines remaining (calculated as total number of mines, minus number of flags the user has placed).
  - Then, it generates the column numbers to print along the top of the game.
  - Finally, it generates the individual rows to be printed.
- `Game.get_column_numbers_to_print` does what the name of the function says it does. Used by `Game.__str__`.
- `Game.generate_rows_to_print` does what the name of the function says it does. Used by `Game.__str__`.
  - Contains a lot of fiddly logic about what to print in which circumstance, depending on game status and the individual square's flagged/cleared status.
  - It would have been simpler if I didn't use emojis, but since I did, I had to do a fair amount of careful whitespace adjustment so everything lines up properly.
- `Game.generate_danger_levels`
- `Game.gameplay_loop`
- `Game.get_point`
- `Game.get_row`
- `Game.get_col`
- `Game.get_action`
- `Game.take_action`
- `Game.recursively_clear`
- `Game.flag`
- `Game.evaluate_status`

##### `generate_mine`

This accepts `width:int` and `height:int` parameters, and returns an `(x, y)` tuple within the field indicated by the `width` and `height` parameters.
Should be moved into the `Game` class.

##### `get_neighbors`

This accepts `point:Tuple[int, int]`, `width:int`, and `height:int` parameters, and returns a `list` of `(x, y)` tuples representing points that are adjacent to the given point, and within the field indicated by the `width` and `height` parameters.
Should be moved into the `Game` class.

##### `count_neighboring_mines`

This accepts `point:Tuple[int, int]` and `game:Game` parameters, and returns an `int` representing how many neighbors of the given `point` have mines on them.
Should be moved into the `Game` class.

##### `clear_screen`

This accepts no parameters, and returns `None`. As a side effect, it clears the terminal. It was taken from `https://www.geeksforgeeks.org/clear-screen-python/`.

##### `main`

This accepts no parameters, and returns `None`. It initializes the game, runs the gameplay loop until the game is over, and prints the final result.

#### TODO:
##### Sooner:
- implement "first clear is always safe" feature!!!
- implement Mark feature
- allow user to set game parameters
  - CLI params
  - In-app prompts if CLI params not provided

##### Later:
- move Game class and various util functions into a separate file
- replace most of this README documentation with docstrings in the actual code
- implement "difficulty levels" instead of (or supplementing) direct setting of game parameters
- implement a GUI - maybe [Pyxel](https://github.com/kitao/pyxel)?
