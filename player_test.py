import pytest
import pygame
from core import Team
from player import Player

def test_player_distance_1():
    p1=Player('red')
    p2=Player('blue')
    p1.rect.move_ip(0,0)
    p2.rect.move_ip(3,4)
    assert(p1.distance(p2)==5)

def test_player_distance_2():
    p1=Player('red')
    p2=Player('blue')
    p1.rect.move_ip(1,0)
    p2.rect.move_ip(21,0)
    assert(p1.distance(p2)==20)

def test_player_distance_typeerror():
    p1=Player('red')
    with pytest.raises(TypeError):
        p1.distance(1)

def test_opposite_1():
    teams = {
        "red": Team(Player("red"), None),
        "blue": Team(Player("blue"), None)
    }
    assert(teams['blue'].player.opposite(teams)==teams['red'].player)

def test_opposite_2():
    teams = {
        "red": Team(Player("red"), None),
        "blue": Team(Player("blue"), None)
    }
    assert(teams['red'].player.opposite(teams)==teams['blue'].player)

def test_opposite_typeerror():
    teams = {
        "red": Team(Player("red"), None),
        "blue": Team(Player("blue"), None)
    }
    with pytest.raises(TypeError):
        teams['red'].player.opposite(1)

def test_is_on_ground_1():
    p1 = Player('red')
    p1.rect.move_ip(10, 10)
    platforms=[pygame.Rect(10,74,10,10)]
    assert(p1.is_on_ground(platforms)==True)

def test_is_on_ground_2():
    p1 = Player('red')
    p1.rect.move_ip(5, 5)
    platforms=[pygame.Rect(10,75,100,100)]
    assert(p1.is_on_ground(platforms)==False)

def test_is_on_ground_typeeror():
    p1=Player('red')
    with pytest.raises(TypeError):
        p1.is_on_ground(1)

def test_is_standing_on_other_player_1():
    p1 = Player('red')
    p1.rect.move_ip(10, 10)
    p2 = Player('blue')
    p2.rect.move_ip(15, 74)
    assert(p1.is_standing_on_other_player(p2)==True)

def test_is_standing_on_other_player_2():
    p1 = Player('red')
    p1.rect.move_ip(10, 10)
    p2 = Player('blue')
    p2.rect.move_ip(15, 75)
    assert(p1.is_standing_on_other_player(p2)==False)

def test_is_standing_on_other_player_typeerror():
    p1 = Player('red')
    p1.rect.move_ip(10, 10)
    with pytest.raises(TypeError):
        p1.is_standing_on_other_player(1)



