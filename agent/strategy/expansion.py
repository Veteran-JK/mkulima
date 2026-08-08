"""
agent/strategy/expansion.py

Farm expansion strategy.
"""

from __future__ import annotations

from agent.strategy.base import Strategy
from agent.tasks import Task
from agent.world import GameState


class ExpansionStrategy(Strategy):

    def propose(
        self,
        state: GameState,
    ) -> Task | None:

        return None