"""
Module with DistributedGreedyBFS class implementation of FindingAlgorithm abstract class
"""

from queue import PriorityQueue
from typing import List

import numpy as np

from app.src.finding_algorithm.base import FindingAlgorithm
from app.src.utils import Utils


class DistributedGreedyBFS(FindingAlgorithm):
    """
    Implementation of abstract class FindingAlgorithm. This finding algorithm finds nearest tile which differs for at least two possible starting positions and therefore by going
    there at least one of possible starting positions is eliminated.
    """

    def __init__(self, environment_map):
        super().__init__(environment_map, 'DistributedGreedyBFS')

    def get_path(self, bot_rel_pos: np.ndarray, bot_rel_dir: np.ndarray) -> List[str]:
        """
        Calculates next part of path
        :param bot_rel_pos:
        :param bot_rel_dir:
        :return: next part of path
        """
        prev = {(0, 0): None}
        pos = np.array([0, 0])
        queue = PriorityQueue()
        queue.put((0, pos))

        end_pos = None

        while not queue.empty():
            priority, pos_delta = queue.get()
            pos_delta = np.array(pos_delta)

            if self.process_node(bot_rel_pos, bot_rel_dir, pos_delta):
                end_pos = pos_delta
                break

            for neighbour in Utils.neighbours:
                neighbour_delta = pos_delta + neighbour

                if tuple(neighbour_delta) not in prev:
                    prev[tuple(neighbour_delta)] = pos_delta

                    # add neighbour_delta to queue if any possible start + neighbour_delta is inside map
                    for pos_and_dir in self.possible_starting_poss:
                        # starting pos + relative delta rotated to expected direction + neighbour delta rotated to bot current abs bot dir
                        pos = pos_and_dir[0] + Utils.rotate_coords(bot_rel_pos, 'left',
                                                                   pos_and_dir[1]) + Utils.rotate_coords(
                            neighbour_delta, 'left', pos_and_dir[1] + Utils.dir_to_number(bot_rel_dir))

                        if 0 <= pos[0] < self.environment_map.shape[0] and 0 <= pos[1] < self.environment_map.shape[
                            1] and \
                                self.environment_map[tuple(pos)] != 0:
                            curr_bot_dir = prev.get(tuple(pos_delta)) - pos_delta if prev.get(
                                tuple(pos_delta)) is not None else Utils.initial_dir
                            rotations = min(abs(Utils.dir_to_number(neighbour) - Utils.dir_to_number(curr_bot_dir)),
                                            4 - abs(Utils.dir_to_number(neighbour) - Utils.dir_to_number(curr_bot_dir)))
                            queue.put((priority + rotations + 1, tuple(neighbour_delta)))
                            break

        if end_pos is None:
            return []

        moves = []

        while prev.get(tuple(end_pos)) is not None:
            moves.append(end_pos - np.asarray(prev.get(tuple(end_pos))))
            end_pos = prev.get(tuple(end_pos))

        moves.reverse()
        return self.get_path_commands_from_moves(moves)

    def process_node(self, bot_rel_pos: np.ndarray, bot_rel_dir: np.ndarray, pos_delta: np.ndarray) -> bool:
        """
        :param bot_rel_pos:
        :param bot_rel_dir:
        :param pos_delta:
        :return: True if search should end and this node is final. False otherwise.
        """
        visible_environments = set()

        for pos_and_dir in self.possible_starting_poss:
            # starting pos + relative delta rotated to expected direction + neighbour delta rotated to bot current abs bot dir
            pos = pos_and_dir[0] + Utils.rotate_coords(bot_rel_pos, 'left', pos_and_dir[1]) + Utils.rotate_coords(
                pos_delta, 'left', pos_and_dir[1] + Utils.dir_to_number(bot_rel_dir))

            if 0 <= pos[0] < self.environment_map.shape[0] and 0 <= pos[1] < self.environment_map.shape[1]:
                visible_environments.add(
                    tuple(self.get_visible_environment(self.environment_map, pos, pos_and_dir[1], 1)))

                if len(visible_environments) > 1:
                    return True

        return len(visible_environments) > 1
