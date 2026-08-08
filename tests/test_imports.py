"""
Basic import tests.

If this file imports successfully, the package structure is healthy.
"""

from agent.world import GameState
from agent.planner import Planner
from agent.actions import Actions
from agent.strategy.scheduler import Scheduler


def test_imports():

    assert GameState is not None
    assert Planner is not None
    assert Actions is not None
    assert Scheduler is not None