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
from agent.tasks import PlantTask, Task
from agent.strategy.base import Strategy
from agent.world import GameState


class FarmingStrategy(Strategy):
    """
    Basic crop-planting strategy.

    The current implementation uses wheat as the first crop
    because the initial farming loop is intended to verify the
    strategy -> task pipeline rather than optimize crop selection.
    """

    def propose(self, state: GameState) -> Task | None:
        """
        Propose a planting task if planting is currently possible.

        The strategy:

        1. Checks whether wheat seeds are available.
        2. Searches the player's farm for an unlocked empty tile.
        3. Returns a PlantTask for the first suitable tile.
        4. Returns None when no planting opportunity exists.
        """

        # No seed means there is nothing this strategy can plant.
        if state.seeds.get("WHEAT", 0) <= 0:
            return None

        farm = state.me

        for row in farm.tiles:
            for tile in row:

                if not tile.is_empty:
                    continue

                return PlantTask(
                    target=tile.position,
                    crop="WHEAT",
                )

        return None