"""
agent/strategy/opening.py

Opening strategy.

Responsible for the initial setup phase of the season.

Current scope:
    - Ensure the agent has wheat seed available.
    - Purchase one wheat seed when none are available and
      sufficient money exists.

This strategy intentionally contains no:
    - action execution
    - pathfinding
    - crop profitability analysis
    - market forecasting
    - expansion logic
    - livestock logic

Those concerns belong to other components.
"""

from __future__ import annotations

from agent.constants import Crop
from agent.strategy.base import Strategy
from agent.tasks import BuySeedTask, Task
from agent.world import GameState


class OpeningStrategy(Strategy):
    """
    Handles the agent's initial setup phase.
    """

    SEED_COST = 10

    def propose(self, state: GameState) -> Task | None:
        """
        Propose the next opening task.

        Current opening behavior:

        1. Check whether wheat seeds are available.
        2. If wheat seeds already exist, do nothing.
        3. If no wheat seeds exist and the player can afford one,
           propose buying one wheat seed.
        4. If the player cannot afford one, return None.

        The strategy only proposes the task. It does not execute
        the market action.
        """

        # Wheat is already available.
        if state.seeds.get(Crop.WHEAT, 0) > 0:
            return None

        # Cannot purchase a seed.
        if state.me.money < self.SEED_COST:
            return None

        # Initial farming setup.
        return BuySeedTask(
            crop=Crop.WHEAT,
            quantity=1,
        )