import os
from contextlib import nullcontext as does_not_raise

import numpy as np
import pytest

from app.src.utils import Utils


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize(
    'coords, direction, count, expected, exception',
    [
        (np.array([10, 10]), 'left', 2, np.array([-10, -10]), does_not_raise()),
        (np.array([10, 10]), 'right', 2, np.array([-10, -10]), does_not_raise()),
        (np.array([10, 10]), 'left', -2, np.array([-10, -10]), does_not_raise()),
        (np.array([10, 10]), 'left', -2, np.array([-10, -10]), does_not_raise()),
        (np.array([10, 10]), 'left', 6, np.array([-10, -10]), does_not_raise()),
        (np.array([10, 10]), 'left', 1, np.array([-10, 10]), does_not_raise()),
        (np.array([10, 10]), 'right', 1, np.array([10, -10]), does_not_raise()),
        (np.array([10, 10]), 'right', 0, np.array([10, 10]), does_not_raise()),
        (np.array([10, 10]), 'left', 0, np.array([10, 10]), does_not_raise()),
        (np.array([10, 10]), 'right', 7, np.array([-10, 10]), does_not_raise()),

        ([10, 10], 'left', 2, np.array([-10, -10]), pytest.raises(ValueError)),
        (np.array([10, 10]), '', 2, np.array([-10, -10]), pytest.raises(ValueError)),
    ]
)
def test_rotate_coords(coords, direction, count, expected, exception):
    with exception:
        assert np.array_equal(Utils.rotate_coords(coords, direction, count), expected)


@pytest.mark.parametrize(
    'coords, expected, exception',
    [
        (np.array([1, 0]), 0, does_not_raise()),
        (np.array([0, 1]), 1, does_not_raise()),
        (np.array([-1, 0]), 2, does_not_raise()),
        (np.array([0, -1]), 3, does_not_raise()),
        (np.array([2, 0]), 0, does_not_raise()),

        (np.array([0, 0]), 0, pytest.raises(ValueError)),
        (np.array([2, 1]), 0, pytest.raises(ValueError)),
        (np.array([1.1, 0.1]), 0, pytest.raises(ValueError)),
    ]
)
def test_dir_to_number(coords, expected, exception):
    with exception:
        assert Utils.dir_to_number(coords) == expected


@pytest.mark.parametrize(
    'direction, expected, exception',
    [
        (0, np.array([1, 0]), does_not_raise()),
        (1, np.array([0, 1]), does_not_raise()),
        (2, np.array([-1, 0]), does_not_raise()),
        (3, np.array([0, -1]), does_not_raise()),
        (7, np.array([0, -1]), does_not_raise()),

        (0.5, np.array([2, 0]), pytest.raises(ValueError))
    ]
)
def test_number_to_dir(direction, expected, exception):
    with exception:
        assert np.array_equal(Utils.number_to_dir(direction), expected)


@pytest.mark.parametrize(
    'num, expected, exception',
    [
        (0, '·', does_not_raise()),
        (1, '╵', does_not_raise()),
        (2, '╷', does_not_raise()),
        (3, '│', does_not_raise()),
        (4, '╴', does_not_raise()),
        (5, '┘', does_not_raise()),
        (6, '┐', does_not_raise()),
        (7, '┤', does_not_raise()),
        (8, '╶', does_not_raise()),
        (9, '└', does_not_raise()),
        (10, '┌', does_not_raise()),
        (11, '├', does_not_raise()),
        (12, '─', does_not_raise()),
        (13, '┴', does_not_raise()),
        (14, '┬', does_not_raise()),
        (15, '┼', does_not_raise()),

        (0.5, '', pytest.raises(ValueError)),
        (-1, '', pytest.raises(ValueError)),
        (16, '', pytest.raises(ValueError)),
    ]
)
def test_num_to_unicode_wall(num, expected, exception):
    with exception:
        assert Utils.num_to_unicode_wall(num) == expected


@pytest.mark.parametrize(
    'file_name, expected, exception',
    [
        (os.path.join(root_dir, 'maps/zum/0.txt'), np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]), does_not_raise()),
        (os.path.join(root_dir, 'maps/zum/4.txt'),
         np.array([[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]]),
         does_not_raise()),

        ('', None, pytest.raises(FileNotFoundError)),
    ]
)
def test_load(file_name, expected, exception):
    with exception:
        assert np.array_equal(Utils.load(file_name), expected)


@pytest.mark.parametrize(
    'direction, expected, exception',
    [
        (1, '→', does_not_raise()),
        (2, '↑', does_not_raise()),
        (3, '←', does_not_raise()),
        (4, '↓', does_not_raise()),
        (5, '→', does_not_raise()),
        (6, '↑', does_not_raise()),
        (np.array([1, 0]), '↓', does_not_raise()),
        (np.array([0, 1]), '→', does_not_raise()),
        (np.array([-1, 0]), '↑', does_not_raise()),
        (np.array([0, - 1]), '←', does_not_raise()),

        (2.5, '', pytest.raises(ValueError)),
    ]
)
def test_dir_to_unicode_arrow(direction, expected, exception):
    with exception:
        assert Utils.dir_to_unicode_arrow(direction) == expected


@pytest.mark.parametrize(
    'string, fg_color, bg_color, end, expected, exception',
    [
        ('abcd', None, None, '\n', '\x1b[0;0mabcd\x1b[0m\n', does_not_raise()),
        ('abcd', None, None, '', '\x1b[0;0mabcd\x1b[0m', does_not_raise()),
        ('abcd', 'green', 'white', '\n', '\x1b[32;47mabcd\x1b[0m\n', does_not_raise()),

        ('abcd', 'asfd', None, '\n', '', pytest.raises(ValueError)),
    ]
)
def test_print_colored(capfd, string, fg_color, bg_color, end, expected, exception):
    with exception:
        Utils.print_colored(string, fg_color=fg_color, bg_color=bg_color, end=end)
        out, err = capfd.readouterr()
        assert out == expected and err == ''


@pytest.mark.parametrize(
    'color, expected, exception',
    [
        ('black', 0, does_not_raise()),
        ('red', 1, does_not_raise()),
        ('green', 2, does_not_raise()),
        ('yellow', 3, does_not_raise()),
        ('blue', 4, does_not_raise()),
        ('magenta', 5, does_not_raise()),
        ('cyan', 6, does_not_raise()),
        ('white', 7, does_not_raise()),

        ('', 0, pytest.raises(ValueError)),
        ('Red', 0, pytest.raises(ValueError)),
        ('blck', 0, pytest.raises(ValueError)),
    ]
)
def test_color_name_to_num(color, expected, exception):
    with exception:
        assert Utils.color_name_to_num(color) == expected
