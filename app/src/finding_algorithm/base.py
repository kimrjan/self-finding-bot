"""
Module with FindingAlgorithm abstract class
"""
from abc import abstractmethod, ABC
from typing import List

import numpy as np

from app.src.utils import Utils


class FindingAlgorithm(ABC):
    """
    Base class for finding algorithms. Helps bot find path to find itself.
    """

    def __init__(self, environment_map, name):
        self.environment_map = environment_map
        self.name = name
        self.possible_starting_poss = None
        self.is_bot_found = False
        self.steps = 0

    def get_path_controller(self, environment_map: np.ndarray, bot_map: np.ndarray, bot_rel_pos: np.ndarray,
                            bot_rel_dir: np.ndarray) -> List[str]:
        """
        :param environment_map: map of the environment
        :param bot_map: environment discovered by the bot
        :param bot_rel_pos: relative position of the bot
        :param bot_rel_dir: relative direction of the bot
        :return: List of next moves
        """
        self.possible_starting_poss = self.find_all_possible_positions(environment_map, bot_map)

        if len(self.possible_starting_poss) == 1:
            self.is_bot_found = True
            return []

        return self.get_path(bot_rel_pos, bot_rel_dir)

    def find_all_possible_positions(self, environment_map: np.ndarray, bot_map: np.ndarray) -> List[tuple]:
        """
        Finds all possible starting positions of bot on environment map using discovered area in bot's map
        :param environment_map: map of the environment
        :param bot_map: environment discovered by the bot
        :return: list tuples in format (possible starting position, possible starting direction as int)
        """
        possible_starting_poss = []
        for rotation in range(4):
            bot_map_rotated = np.rot90(bot_map, k=rotation)
            not_null = np.where(bot_map_rotated >= 0)
            start_row = np.min(not_null[0])
            end_row = np.max(not_null[0]) + 1

            start_column = np.min(not_null[1])
            end_column = np.max(not_null[1]) + 1

            start = np.array([start_row, start_column])

            discovered_map = bot_map_rotated[start_row:end_row, start_column:end_column]

            delta = bot_map.shape[0] // 2 - start
            possible_starting_poss += [(location + delta, (Utils.dir_to_number(Utils.initial_dir) + rotation) % 4) for
                                       location in self.find_matrix_placements(environment_map, discovered_map)]

        return possible_starting_poss

    def possible_starting_poss_to_str(self) -> str:
        """
        :return: string of possible starting position in readable format
        """
        return '; '.join([f'({pos_and_dir[0]} {Utils.dir_to_unicode_arrow(pos_and_dir[1])})' for pos_and_dir in
                          self.possible_starting_poss])

    def possible_current_poss(self, bot_rel_pos: np.ndarray, bot_rel_dir: np.ndarray) -> List[tuple]:
        """
        :param bot_rel_pos:
        :param bot_rel_dir:
        :return: List of possible current positions of the bot (possible starting position, possible starting direction as int)
        """
        return [(pos_and_dir[0] + Utils.rotate_coords(bot_rel_pos, "left", pos_and_dir[1]),
                 (pos_and_dir[1] + Utils.dir_to_number(bot_rel_dir)) % 4)
                for pos_and_dir in self.possible_starting_poss]

    def possible_current_poss_to_str(self, bot_rel_pos: np.ndarray, bot_rel_dir: np.ndarray) -> str:
        """
        :return: string of possible starting position in readable format
        """

        return '; '.join([f'({pos_and_dir[0]} {Utils.dir_to_unicode_arrow(pos_and_dir[1])})' for pos_and_dir in
                          self.possible_current_poss(bot_rel_pos, bot_rel_dir)])

    @staticmethod
    def get_visible_environment(environment_map: np.ndarray, bot_pos: np.ndarray, bot_dir: np.ndarray,
                                sight_range: int) -> np.ndarray:
        """
        Returns environment visible to bot rotated according to specified bot rotation and in sight range.
        :param environment_map:
        :param bot_pos:
        :param bot_dir:
        :param sight_range:
        :return: 1D np.array of visible environment. Visible environment after using ravel().
        """
        return np.rot90(environment_map[
                        max(bot_pos[0] - sight_range, 0): min(bot_pos[0] + sight_range + 1, environment_map.shape[0]),
                        max(bot_pos[1] - sight_range, 0): min(bot_pos[1] + sight_range + 1, environment_map.shape[1])],
                        k=-bot_dir).ravel()

    @staticmethod
    def find_matrix_placements(matrix: np.ndarray, matrix_to_find: np.ndarray) -> List[np.ndarray]:
        """
        :param matrix: must be bigger than matrix_to_find
        :param matrix_to_find: matrix to find locations of
        :return: list of top-left positions from which values of matrix and matrix_to_find are same
        """
        rows_cnt, cols_cnt = matrix.shape
        inner_rows_cnt, inner_cols_cnt = matrix_to_find.shape

        matches = []

        for i in range(rows_cnt - inner_rows_cnt + 1):
            for j in range(cols_cnt - inner_cols_cnt + 1):
                # positions where numbers differ
                not_equal_positions = np.where(matrix_to_find != matrix[i:i + inner_rows_cnt, j:j + inner_cols_cnt])

                # check if all numbers that differ are -1
                if np.all(matrix_to_find[not_equal_positions] == -1):
                    matches.append(np.array([i, j]))

        return matches

    @abstractmethod
    def get_path(self, bot_rel_pos, bot_rel_dir) -> List[str]:
        """
        Calculates next part of path
        :param bot_rel_pos:
        :param bot_rel_dir:
        :return: next part of path
        """

    @staticmethod
    def get_path_commands_from_moves(moves: List[np.ndarray]) -> List[str]:
        """
        :param moves: list of direction of next move
        :return: list of commands "move", "left" and "right"
        """
        prev_dir = Utils.initial_dir
        commands = []

        for curr_dir in moves:
            rotation_diff = (Utils.dir_to_number(curr_dir) - Utils.dir_to_number(prev_dir)) % 4
            if rotation_diff == 0:
                commands.append("move")
            elif rotation_diff == 1:
                commands.append("left")
                commands.append("move")
            elif rotation_diff == 2:
                commands.append("right")
                commands.append("right")
                commands.append("move")
            elif rotation_diff == 3:
                commands.append("right")
                commands.append("move")
            else:
                raise ValueError(f'Unknown rotation: {rotation_diff}')

            prev_dir = curr_dir

        return commands
