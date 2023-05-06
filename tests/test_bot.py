import os

import numpy as np
import pytest

from app.src.bot import Bot
from app.src.environment import Environment
from app.src.utils import Utils


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, direction, bot_expected_dir, bot_expected_rel_dir',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 'left', np.array([0, 1]),
         np.array([0, 1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, 1]), 'left', np.array([-1, 0]),
         np.array([0, 1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([-1, 0]), 'left', np.array([0, -1]),
         np.array([0, 1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, -1]), 'left', np.array([1, 0]),
         np.array([0, 1])),

        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 'right', np.array([0, -1]),
         np.array([0, -1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, 1]), 'right', np.array([1, 0]),
         np.array([0, -1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([-1, 0]), 'right', np.array([0, 1]),
         np.array([0, -1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, -1]), 'right', np.array([-1, 0]),
         np.array([0, -1])),
    ]
)
def test_bot_rotate(environment_map, bot_pos, bot_dir, direction, bot_expected_dir, bot_expected_rel_dir):
    environment = Environment(environment_map, bot_pos, bot_dir)
    bot = Bot(environment)

    bot.rotate(direction)

    assert np.array_equal(environment.bot_dir, bot_expected_dir) and \
           np.array_equal(bot.relative_dir, bot_expected_rel_dir)


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, bot_expected_pos, bot_expected_rel_pos',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), np.array([1, 1]), np.array([0, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([2, 1]), np.array([1, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([2, 1]), np.array([1, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([-1, 0]), np.array([1, 1]), np.array([0, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([0, 1]), np.array([1, 2]), np.array([1, 0])),
    ]
)
def test_environment_move(environment_map, bot_pos, bot_dir, bot_expected_pos, bot_expected_rel_pos):
    environment = Environment(environment_map, bot_pos, bot_dir)
    bot = Bot(environment)

    bot.move()

    assert np.array_equal(environment.bot_pos, bot_expected_pos) and \
           np.array_equal(bot.relative_pos, bot_expected_rel_pos)


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/26.txt')), np.array([1, 1]), np.array([1, 0])),
    ]
)
def test_find_itself(environment_map, bot_pos, bot_dir):
    environment = Environment(environment_map, bot_pos, bot_dir)
    bot = Bot(environment)

    pos = bot.find_itself()[0]
    assert environment.check_position(pos[0])


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, expected',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 9),
    ]
)
def test_get_discovered_tiles_count(environment_map, bot_pos, bot_dir, expected):
    environment = Environment(environment_map, bot_pos, bot_dir)
    bot = Bot(environment)

    assert bot.get_discovered_tiles_count() == 0
    bot.find_itself()
    assert bot.get_discovered_tiles_count() == 9
