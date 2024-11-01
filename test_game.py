from game import Game

def test_count_neighboring_mines():
    game = Game(5, 5)
    game._mines = set(((2, 2), (3, 2), (4, 2), (2, 3), (4, 3), (2, 4), (3, 4), (4, 4)))
    assert game.count_neighboring_mines((0, 0)) == 0
    assert game.count_neighboring_mines((3, 3)) == 8
    assert game.count_neighboring_mines((2, 1)) == 2
    assert game.count_neighboring_mines((1, 1)) == 1
