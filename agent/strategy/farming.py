"""
agent/strategy/farming.py

Basic crop farming strategy.

Sprint 2.1:
    Identify an unlocked empty tile and propose planting wheat.

This strategy intentionally contains no:
    - pathfinding
    - action execution
    - market optimization
    - crop profitability analysis
    - expansion logic

Those concerns belong to other components.
"""

from __future__ import annotations

from agent.models.position import Position
from agent.tasks import PlantTask, WaterTask,Task
from agent.strategy.base import Strategy
from agent.world import GameState
from agent.constants import Crop

class FarmingStrategy(Strategy):
    """
    Basic crop-planting strategy.

    The current implementation uses wheat as the first crop
    because the initial farming loop is intended to verify the
    strategy -> task pipeline rather than optimize crop selection.
    """

    def propose(self, state: GameState) -> Task | None:
        """
        Propose the highest-priority farming task.

        Priority:
        1. Water an existing plant that has not been watered today.
        2. Plant wheat if wheat seeds are available.
        3. Return None when neither action is possible.
        """

        farm = state.me

        # --------------------------------------------------------
        # Priority 1: water existing crops
        # --------------------------------------------------------

        for row in farm.tiles:
            for tile in row:

                if not tile.has_plant:
                    continue

                if tile.occupant is not None and tile.occupant.needs_water:
                    return WaterTask(
                        target=tile.position,
                    )

        # --------------------------------------------------------
        # Priority 2: plant wheat
        # --------------------------------------------------------

        if state.seeds.get("WHEAT", 0) <= 0:
            return None

        for row in farm.tiles:
            for tile in row:

                if not tile.is_empty:
                    continue

                return PlantTask(
                    target=tile.position,
                    crop=Crop.WHEAT,
                )

        return None