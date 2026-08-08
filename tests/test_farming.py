"""
Tests for the farming strategy.
"""

from kaggle_environments import make

from agent.constants import Crop
from agent.strategy.farming import FarmingStrategy
from agent.tasks import PlantTask
from agent.world import GameState


def get_farming_state() -> GameState:
    """
    Build a real GameState from Kaggriculture and provide
    the wheat seed required for planting.
    """

    env = make("kaggriculture", debug=True)

    observations = env.reset()
    observation = observations[0].observation

    state = GameState.from_observation(
        observation,
        env.configuration,
    )

    # The real reset state contains zero seeds.
    # Seed acquisition is tested separately by OpeningStrategy.
    state.seeds[Crop.WHEAT] = 1

    return state


def test_farming_strategy_proposes_planting_task():
    """
    Verify that FarmingStrategy proposes planting when
    wheat seed is available.
    """

    state = get_farming_state()

    strategy = FarmingStrategy()

    task = strategy.propose(state)

    assert task is not None
    assert isinstance(task, PlantTask)


def test_farming_task_targets_empty_tile():
    """
    Verify that the planting task targets an unlocked empty tile.
    """

    state = get_farming_state()

    strategy = FarmingStrategy()

    task = strategy.propose(state)

    assert task is not None
    assert isinstance(task, PlantTask)

    tile = state.me.tile_at(task.target)

    assert tile.unlocked
    assert tile.is_empty


def test_farming_task_uses_wheat():
    """
    Verify that the initial farming strategy proposes wheat.
    """

    state = get_farming_state()

    strategy = FarmingStrategy()

    task = strategy.propose(state)

    assert task is not None
    assert isinstance(task, PlantTask)
    assert task.crop == Crop.WHEAT