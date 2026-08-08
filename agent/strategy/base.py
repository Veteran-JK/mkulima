"""
agent/strategy/base.py

Defines the abstract interface implemented by every strategy.

A strategy examines the current GameState and proposes a single
task within its area of responsibility.

Strategies are decision makers only.

They DO NOT:
    - execute actions
    - perform movement
    - perform pathfinding
    - modify the game state

They simply answer:

    "Given the current state, what is the most valuable task
     in my domain?"
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agent.tasks import Task
from agent.world import GameState


class Strategy(ABC):
    """
    Base class for every strategy.

    Each concrete strategy owns one decision domain, for example:

        - Opening
        - Farming
        - Livestock
        - Market
        - Expansion
        - Economy
        - Emergency
    """

    @property
    def name(self) -> str:
        """
        Human-readable strategy name.
        """
        return self.__class__.__name__

    def __call__(
        self,
        state: GameState,
    ) -> Task | None:
        """
        Allow strategies to be called like functions.

        Example
        -------
        task = strategy(state)
        """
        return self.propose(state)

    @abstractmethod
    def propose(
        self,
        state: GameState,
    ) -> Task | None:
        """
        Propose a task for the current turn.

        Parameters
        ----------
        state : GameState
            Current parsed game state.

        Returns
        -------
        Task | None

            Task
                A proposed task if useful work exists.

            None
                This strategy has nothing useful to contribute
                during the current turn.
        """
        raise NotImplementedError(
            "Strategies must implement propose()."
        )