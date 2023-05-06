import os

import numpy as np
import pytest

from app.src.bot import Bot
from app.src.environment import Environment
from app.src.utils import Utils


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, direction, expected',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 'left', np.array([0, 1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, 1]), 'left', np.array([-1, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([-1, 0]), 'left', np.array([0, -1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, -1]), 'left', np.array([1, 0])),

        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 'right', np.array([0, -1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, 1]), 'right', np.array([1, 0])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([-1, 0]), 'right', np.array([0, 1])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([0, -1]), 'right', np.array([-1, 0])),
    ]
)
def test_environment_rotate(environment_map, bot_pos, bot_dir, direction, expected):
    environment = Environment(environment_map, bot_pos, bot_dir)
    environment.rotate(direction)

    assert np.array_equal(environment.bot_dir, expected)


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, new_bot_pos, ret',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), None, None, np.array([1, 1]), False),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([2, 1]), True),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([2, 1]), True),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([-1, 0]), np.array([1, 1]), False),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([0, 1]), np.array([1, 2]), True),
    ]
)
def test_environment_move(environment_map, bot_pos, bot_dir, new_bot_pos, ret):
    environment = Environment(environment_map, bot_pos, bot_dir)
    assert environment.move() == ret and np.array_equal(environment.bot_pos, new_bot_pos)


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, sight_range, expected_bot_map',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 0,
         np.array([[-1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, 1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1]])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), 2,
         np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1],
                   [-1, -1, -1, -1, 0, 1, 0, -1, -1, -1, -1],
                   [-1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([-1, 0]), 1,
         np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, 1, 1, 0, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, 1, 1, 0, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.]])),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 2]), np.array([1, 0]), 2,
         np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, 0, 1, 1, 1, 0, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, 0, 1, 1, 1, 0, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]))
    ]
)
def test_get_nearby_environment(environment_map, bot_pos, bot_dir, sight_range, expected_bot_map):
    environment = Environment(environment_map, bot_pos, bot_dir)
    bot = Bot(environment, sight_range)

    environment.get_nearby_environment(bot.bot_map, bot.relative_pos + np.asarray(bot.bot_map.shape) // 2, sight_range)
    assert np.array_equal(bot.bot_map, expected_bot_map)


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, possible_current_poss, expected',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), [],
         '\x1b[0;0m┌\x1b[0m\x1b[0;0m─\x1b[0m\x1b[0;0m┐\x1b[0m\n\x1b[0;0m│\x1b[0m\x1b[30;0m↓\x1b[0m\x1b[0;0m│\x1b[0m\n\x1b[0;0m└\x1b[0m\x1b[0;0m─\x1b[0m\x1b[0;0m┘\x1b[0m\nLegend:\n\x1b[30;43m↓\x1b[0m - bot\n\x1b[30;43m \x1b[0m - possible bot position\n'),
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), [((1, 1), 1)],
         '\x1b[0;0m┌\x1b[0m\x1b[0;0m─\x1b[0m\x1b[0;0m┐\x1b[0m\n\x1b[0;0m│\x1b[0m\x1b[30;43m↓\x1b[0m\x1b[0;0m│\x1b[0m\n\x1b[0;0m└\x1b[0m\x1b[0;0m─\x1b[0m\x1b[0;0m┘\x1b[0m\nLegend:\n\x1b[30;43m↓\x1b[0m - bot\n\x1b[30;43m \x1b[0m - possible bot position\n'),
    ]
)
def test_print_map(capfd, environment_map, bot_pos, bot_dir, possible_current_poss, expected):
    environment = Environment(environment_map, bot_pos, bot_dir)

    environment.print_map(possible_current_poss)
    out, err = capfd.readouterr()
    assert out == expected and err == ''


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, path, steps, possible_current_positions_string, discovered_tiles, expected',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), [], 0, '', 0,
         'Bot\nPosition and direction: ([1 1] ↓)\nMoves to do: []\nSteps: 0\nPossible current positions: \nDiscovered tiles: 0\n--------------------------------------------------------------------------------\n'),
    ]
)
def test_print_bot_stats(capfd, environment_map, bot_pos, bot_dir, path, steps, possible_current_positions_string, discovered_tiles,
                         expected):
    environment = Environment(environment_map, bot_pos, bot_dir)

    environment.print_bot_stats(path, steps, possible_current_positions_string, discovered_tiles)
    out, err = capfd.readouterr()
    assert out == expected and err == ''


@pytest.mark.parametrize(
    'environment_map, bot_pos, bot_dir, test_bot_pos, test_bot_dir, ret',
    [
        (Utils.load(os.path.join(root_dir, 'maps/zum/0.txt')), np.array([1, 1]), np.array([1, 0]), np.array([1, 1]), np.array([1, 0]), True),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([1, 0]),
         np.array([1, 0]), False),
        (Utils.load(os.path.join(root_dir, 'maps/zum/4.txt')), np.array([1, 1]), np.array([1, 0]), np.array([1, 1]),
         np.array([-1, 0]), False)
    ]
)
def test_check_position(environment_map, bot_pos, bot_dir, test_bot_pos, test_bot_dir, ret):
    environment = Environment(environment_map, bot_pos, bot_dir)
    assert environment.check_position((test_bot_pos, Utils.dir_to_number(test_bot_dir))) == ret

