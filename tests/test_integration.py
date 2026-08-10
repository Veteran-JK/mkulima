"""
Integration tests for the Mkulima agent.

These tests use the real Kaggriculture environment rather than
hand-built state fixtures.
"""

import importlib
import pytest

try:
    kaggle_environments = importlib.import_module("kaggle_environments")
    make = kaggle_environments.make
except ImportError:
    pytest.skip("kaggle_environments is required for integration tests", allow_module_level=True)

from agent.planner import Planner
from agent.world import GameState


def get_initial_environment():
    """Create and reset a real Kaggriculture environment."""
    env = make("kaggriculture", debug=True)
    observations = env.reset()

    return env, observations


def test_opening_purchase_against_real_environment():
    """
    Verify that the opening strategy can purchase wheat seed
    through the real Kaggriculture environment.
    """

    env, observations = get_initial_environment()

    observation = observations[0].observation
    configuration = env.configuration

    state = GameState.from_observation(
        observation,
        configuration,
    )

    # Initial environment state.
    assert state.seeds["WHEAT"] == 0
    assert state.me.money == 3000.0

    planner = Planner(state)

    actions = planner.plan()

    # The opening strategy should request one wheat seed.
    assert actions["market"] == [
        ["BUY_SEED", "WHEAT", 1]
    ]

    # Submit our action against the real environment.
    observations = env.step([
        actions,
        {
            "farmer": ["PASS"],
            "hands": [],
            "market": [],
        },
    ])

    after = observations[0].observation

    # Verify the actual environment state changed.
    assert after["private"]["seeds"]["WHEAT"] == 1
    assert after["farms"][0]["money"] == 2990.0

def test_seed_purchase_then_farming_against_real_environment():
    """
    Verify the transition from the opening phase into farming
    using the real Kaggriculture environment.
    """

    env, observations = get_initial_environment()

    # --------------------------------------------------
    # Turn 0: build state from the real observation
    # --------------------------------------------------

    observation = observations[0].observation
    state = GameState.from_observation(
        observation,
        env.configuration,
    )

    planner = Planner(state)

    purchase_actions = planner.plan()

    assert purchase_actions["market"] == [
        ["BUY_SEED", "WHEAT", 1]
    ]

    # --------------------------------------------------
    # Execute the real market action
    # --------------------------------------------------

    observations = env.step([
        purchase_actions,
        {
            "farmer": ["PASS"],
            "hands": [],
            "market": [],
        },
    ])

    # --------------------------------------------------
    # Turn 1: rebuild state from the new real observation
    # --------------------------------------------------

    observation = observations[0].observation

    state = GameState.from_observation(
        observation,
        env.configuration,
    )

    assert state.seeds["WHEAT"] == 1

    # --------------------------------------------------
    # Planner should now transition to farming
    # --------------------------------------------------

    planner = Planner(state)

    actions = planner.plan()

    # The farmer starts at (0, 0), and the first empty
    # unlocked tile should be (0, 0).
    
    farmer_position = state.me.farmer.position

    # The farming strategy selects the first available
    # unlocked empty tile.
    target = None

    for row in state.me.tiles:
        for tile in row:
            if tile.is_empty:
                target = tile.position
                break
        if target is not None:
            break

    assert target is not None
    assert actions["market"] == []