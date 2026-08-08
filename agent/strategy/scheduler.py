"""
agent/strategy/scheduler.py

Coordinates all strategy modules.

The scheduler queries each strategy in priority order and
returns the first task that should be executed.
"""

from __future__ import annotations

from agent.tasks import Task, WaitTask
from agent.world import GameState

from agent.strategy.base import Strategy
from agent.strategy.emergency import EmergencyStrategy
from agent.strategy.opening import OpeningStrategy
from agent.strategy.farming import FarmingStrategy
from agent.strategy.livestock import LivestockStrategy
from agent.strategy.market import MarketStrategy
from agent.strategy.expansion import ExpansionStrategy
from agent.strategy.economy import EconomyStrategy


class Scheduler:
    """
    Coordinates all strategies.

    Strategies are evaluated from highest priority to lowest.

    The first strategy that proposes a task wins.
    """

    def __init__(self) -> None:

        self.strategies: list[Strategy] = [

            EmergencyStrategy(),

            OpeningStrategy(),

            FarmingStrategy(),

            LivestockStrategy(),

            MarketStrategy(),

            EconomyStrategy(),

            ExpansionStrategy(),
        ]

    def choose_task(
        self,
        state: GameState,
    ) -> Task:

        for strategy in self.strategies:

            task = strategy(state)

            if task is not None:
                return task

        return WaitTask()