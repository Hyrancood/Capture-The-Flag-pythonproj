"""Тесты core"""
import pytest

import core
from core import *


def test_rect_to_str_1():
    assert (rect_to_str(pygame.Rect(1, 2, 3, 4)) == '1,2,3,4')


def test_rect_to_str_typeerror():
    with pytest.raises(TypeError):
        rect_to_str(1)


def test_str_to_rect_1():
    assert (str_to_rect('1,2,3,4') == pygame.Rect(1, 2, 3, 4))


def test_str_to_rect_typeerror():
    with pytest.raises(TypeError):
        str_to_rect(1)


def test_str_to_rect_valueerror():
    with pytest.raises(ValueError):
        str_to_rect('1,2,3,!')


def test_array_of_rects_to_str_1():
    rect_list = [pygame.Rect(1, 2, 3, 4), pygame.Rect(10, 9, 8, 7), pygame.Rect(11, 12, 13, 14)]
    assert (array_of_rects_to_str(rect_list) == '1,2,3,4;10,9,8,7;11,12,13,14')


def test_array_of_rects_to_str_2():
    rect_list = []
    assert (array_of_rects_to_str(rect_list) == '')


def test_array_of_rects_to_str_typeerror():
    with pytest.raises(TypeError):
        array_of_rects_to_str(1)


def test_str_to_array_of_rects_1():
    assert (str_to_array_of_rects('1,2,3,4;5,6,7,8') == [pygame.Rect(1, 2, 3, 4), pygame.Rect(5, 6, 7, 8)])


def test_str_to_array_of_rects_typeerror():
    with pytest.raises(TypeError):
        str_to_array_of_rects(1)


def test_str_to_array_of_rects_valueerror():
    with pytest.raises(ValueError):
        str_to_array_of_rects('1,2,3,4;1,2')


def test_team_to_str_1():
    p1 = Player('red')
    team = core.Team(p1, core.Flag(0, 0, 'red', pygame.Rect(0, 0, 16, 48)))
    assert (team_to_str(team) == '0,0,16,48-0,0,32,64-')


def test_team_to_str_typeerror():
    with pytest.raises(TypeError):
        str_to_team(1)


def test_str_to_team_1():
    p1 = Player('red')
    team = core.Team(p1, core.Flag(0, 0, 'red', pygame.Rect(0, 0, 16, 48)))
    assert (str_to_team('0,0,16,48-0,0,32,64-', 'red').flag.color == team.flag.color)
    assert (str_to_team('0,0,16,48-0,0,32,64-', 'red').player.rect == team.player.rect)


def test_str_to_team_typeerror():
    with pytest.raises(TypeError):
        str_to_team(1, 1)


def test_str_to_team_valuerror():
    with pytest.raises(ValueError):
        str_to_team('', '')
