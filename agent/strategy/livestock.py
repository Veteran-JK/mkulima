"""
agent/strategy/livestock.py

Animal management strategy.
"""

from __future__ import annotations

from agent.strategy.base import Strategy
from agent.tasks import Task
from agent.world import GameState


class LivestockStrategy(Strategy):

    def propose(
        self,
        state: GameState,
    ) -> Task | None:

        return None