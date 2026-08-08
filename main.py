"""
main.py

Entry point for the Kaggriculture agent.
"""

from __future__ import annotations

from agent.world import GameState
from agent.planner import Planner


def agent(observation, configuration):
    """
    Kaggle entry point.

    Parameters
    ----------
    observation
        Current game observation.

    configuration
        Environment configuration.

    Returns
    -------
    dict
        Action dictionary expected by Kaggle.
    """

    state = GameState.from_observation(
        observation,
        configuration,
    )

    planner = Planner(state)

    return planner.plan()