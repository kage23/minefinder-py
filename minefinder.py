from game import Game
from utils import clear_screen

def main():
    game = Game(10, 10, 10)
    while game.status == 0:
        game._gameplay_loop()
    clear_screen()
    print(game)
    print("You win" if game.status == 1 else "You lose")


if __name__ == "__main__":
    main()
