import os
import random

from game_types import Point

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


