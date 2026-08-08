"""
Tests for the opening strategy.
"""

import importlib
import pytest

# Import kaggle_environments dynamically to avoid static analysis issues
try:
    make = importlib.import_module("kaggle_environments").make
except ImportError:
    pytest.skip("kaggle_environments is required for these tests", allow_module_level=True)

from agent.constants import Crop
from agent.strategy.opening import OpeningStrategy
from agent.tasks import BuySeedTask
from agent.world import GameState


def get_initial_state() -> GameState:
    """Build a GameState from the real Kaggriculture reset."""
    env = make("kaggriculture", debug=True)

    observations = env.reset()
    observation = observations[0].observation

    return GameState.from_observation(
        observation,
        env.configuration,
    )


def test_opening_strategy_buys_wheat_seed():
    """
    The initial Kaggriculture state has no wheat seeds,
    so the opening strategy should propose buying one.
    """

    state = get_initial_state()

    strategy = OpeningStrategy()
    task = strategy.propose(state)

    assert task is not None
    assert isinstance(task, BuySeedTask)
    assert task.crop == Crop.WHEAT
    assert task.quantity == 1


def test_opening_strategy_does_nothing_when_seed_exists():
    """
    Once wheat seed is available, the opening strategy
    should no longer propose another purchase.
    """

    state = get_initial_state()

    # Simulate the prerequisite having already been acquired.
    state.seeds[Crop.WHEAT] = 1

    strategy = OpeningStrategy()
    task = strategy.propose(state)

    assert task is None