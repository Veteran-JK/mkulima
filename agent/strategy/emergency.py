"""
agent/strategy/emergency.py

Emergency strategy.

Handles situations that threaten the survival of the farm.
"""

from __future__ import annotations

from agent.strategy.base import Strategy
from agent.tasks import Task
from agent.world import GameState


class EmergencyStrategy(Strategy):

    def propose(
        self,
        state: GameState,
    ) -> Task | None:

        return None