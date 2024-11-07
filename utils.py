import os, random

def generate_mine(width:int, height:int) -> str:
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    return f"{x},{y}"


def get_neighbors(point:str, width:int, height:int) -> list[str]:
    x, y = map(int, point.split(","))
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0), # 4-way
        (1, 1), (1, -1), (-1, 1), (-1, -1) # Diagonals
    ]
    return list(map(
        lambda n: f"{n[0]},{n[1]}",
        list(filter(
          lambda n: 0 <= n[0] < width and 0 <= n[1] < height,
          map(lambda d: (x + d[0], y + d[1]), directions)
        ))
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
