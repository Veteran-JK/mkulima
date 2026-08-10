"""
agent/planner.py

Coordinates decision making for a single game turn.

The Planner:
    1. asks the Scheduler for a task,
    2. translates that task into an environment action,
    3. returns the action dictionary expected by Kaggriculture.

Strategy decides WHAT to do.
Planner decides HOW to express that decision as an action.
"""

from __future__ import annotations

from agent.actions import Actions, buy_seed, move, plant, wait
from agent.pathing import next_step
from agent.strategy.scheduler import Scheduler
from agent.tasks import BuySeedTask, PlantTask, WaitTask
from agent.world import GameState
from agent.models.position import Position


class Planner:
    """
    Coordinates execution for one turn.
    """

    def __init__(self, state: GameState) -> None:
        self.state = state
        self.scheduler = Scheduler()

    def plan(self) -> dict:
        """
        Produce the action dictionary for the current turn.

        Supported tasks:

            WaitTask
                -> PASS

            BuySeedTask
                -> BUY_SEED market action

            PlantTask
                -> PLANT if already at target
                -> MOVE toward target otherwise

        Unsupported tasks currently fall back to PASS.
        """

        task = self.scheduler.choose_task(self.state)

        actions = Actions()

        if task is None:
            actions.farmer = wait()
            return actions.to_dict()

        # --------------------------------------------------
        # Wait
        # --------------------------------------------------

        if isinstance(task, WaitTask):
            actions.farmer = wait()
            return actions.to_dict()

        # --------------------------------------------------
        # Market: buy seeds
        # --------------------------------------------------

        if isinstance(task, BuySeedTask):
            actions.market.append(
                buy_seed(
                    task.crop,
                    task.quantity,
                )
            )

            return actions.to_dict()

        # --------------------------------------------------
        # Farming: plant crop
        # --------------------------------------------------

        if isinstance(task, PlantTask):

            current = self.state.me.farmer.position
            target = task.target

            # Already standing on the target tile.
            if current == target:
                actions.farmer = plant(task.crop)
                return actions.to_dict()

            # Otherwise find the next movement direction.
            direction = next_step(
                start=current,
                goal=target,
                tile_at=lambda x, y: self.state.me.tile_at(
                    Position(x, y)
                ),
                board_size=self.state.me.width,
            )

            # No path exists.
            if direction is None:
                actions.farmer = wait()
                return actions.to_dict()

            actions.farmer = move(direction)

            return actions.to_dict()

        # --------------------------------------------------
        # Unsupported task
        # --------------------------------------------------

        actions.farmer = wait()

        return actions.to_dict()