import inspect

import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter

from app.src.bot import Bot
from app.src.environment import Environment
from app.src.finding_algorithm.base import FindingAlgorithm
from app.src.finding_algorithm.distributed_greedy_bfs import DistributedGreedyBFS
from app.src.utils import Utils


# modified code from hw04
@pytest.fixture(scope="session")
def linter_and_score():
    """ Test codestyle for src file of render_tree fucntion. """
    src_files = [inspect.getfile(Bot), inspect.getfile(Environment), inspect.getfile(Utils),
                 inspect.getfile(FindingAlgorithm), inspect.getfile(DistributedGreedyBFS)]

    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    r = None
    score = 0
    for file in src_files:
        r = Run(['--disable=C0301,C0103 ', '-sn', file], reporter=rep, exit=False)
        score += r.linter.stats.global_note / len(src_files)

    return r.linter, score


@pytest.mark.parametrize("limit", range(0, 11))
def test_codestyle_score(linter_and_score, limit, runs=[]):
    """ Evaluate codestyle for different thresholds. """
    if len(runs) == 0:
        print('\nLinter output:')
        for m in linter_and_score[0].reporter.messages:
            print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
    runs.append(limit)
    score = linter_and_score[1]

    print(f'pylint score = {score} limit = {limit}')
    assert score >= limit


