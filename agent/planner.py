"""
agent/planner.py

Coordinates decision making for a single game turn.

The Planner does not decide strategy.
It asks the Scheduler for a task, then converts that task into
actions understood by the Kaggle environment.
"""

from __future__ import annotations

from agent.actions import Actions, wait
from agent.strategy.scheduler import Scheduler
from agent.tasks import WaitTask
from agent.world import GameState


class Planner:
    """
    Coordinates execution for one turn.
    """

    def __init__(
        self,
        state: GameState,
    ) -> None:

        self.state = state
        self.scheduler = Scheduler()

    def plan(self) -> dict:
        """
        Produce the action dictionary for the current turn.
        """

        # --------------------------------------------------
        # Step 1
        # Ask the strategy layer for the highest-priority task.
        # --------------------------------------------------

        task = self.scheduler.choose_task(self.state)

        # --------------------------------------------------
        # Step 2
        # (Future)
        #
        # Translate the task into movement using the pathfinder.
        # --------------------------------------------------

        # --------------------------------------------------
        # Step 3
        # (Future)
        #
        # Translate movement/task into Kaggle actions.
        # --------------------------------------------------

        actions = Actions()

        # Current milestone:
        # Every strategy returns None,
        # therefore Scheduler returns WaitTask.

        if isinstance(task, WaitTask):
            actions.farmer = wait()

        else:
            # Placeholder until task execution exists.
            actions.farmer = wait()

        # --------------------------------------------------
        # Step 4
        # Return the Kaggle action dictionary.
        # --------------------------------------------------

        return actions.to_dict()