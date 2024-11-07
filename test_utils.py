from utils import (
    generate_mine,
    get_neighbors,
)

def test_generate_mine():
    # Since this function uses random numbers, let's run the test several times
    for _ in range(50):
        mine = generate_mine(5, 5)
        x, y = map(int, mine.split(","))
        assert 0 <= x < 5 and 0 <= y < 5


def test_get_neighbors():
    point = "0,0"
    neighbors = get_neighbors(point, 3, 3)
    assert len(neighbors) == 3
    assert "0,1" in neighbors
    assert "1,0" in neighbors
    assert "1,1" in neighbors

    point = "3,3"
    neighbors = get_neighbors(point, 4, 4)
    assert len(neighbors) == 3
    assert "3,2" in neighbors
    assert "2,3" in neighbors
    assert "2,2" in neighbors

    point = "2,2"
    neighbors = get_neighbors(point, 4, 4)
    assert len(neighbors) == 8
    assert "1,1" in neighbors
    assert "2,1" in neighbors
    assert "3,1" in neighbors
    assert "1,2" in neighbors
    assert "3,2" in neighbors
    assert "1,3" in neighbors
    assert "2,3" in neighbors
    assert "3,3" in neighbors

