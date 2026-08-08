"""
agent/tasks.py

Task definitions used by the planner.

A Strategy decides WHICH task should be executed.
The Planner decides HOW to execute it.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.constants import (
    Animal,
    Crop,
    Product,
    Quadrant,
)

from agent.models.position import Position


# ============================================================
# Base Task
# ============================================================


@dataclass(slots=True)
class Task:
    """
    Base class for every task.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__


# ============================================================
# Spatial Tasks
# ============================================================


@dataclass(slots=True)
class FarmTask(Task):
    """
    A task requiring movement to a farm tile.
    """

    target: Position


# ============================================================
# Movement
# ============================================================


@dataclass(slots=True)
class MoveTask(FarmTask):
    """
    Move to a destination.
    """


# ============================================================
# Crops
# ============================================================


@dataclass(slots=True)
class PlantTask(FarmTask):
    crop: Crop


@dataclass(slots=True)
class WaterTask(FarmTask):
    pass


@dataclass(slots=True)
class HarvestTask(FarmTask):
    pass


@dataclass(slots=True)
class FertilizeTask(FarmTask):
    pass


@dataclass(slots=True)
class DigTask(FarmTask):
    pass


# ============================================================
# Animals
# ============================================================


@dataclass(slots=True)
class FeedTask(FarmTask):
    pass


@dataclass(slots=True)
class CareTask(FarmTask):
    pass


@dataclass(slots=True)
class CollectFertilizerTask(FarmTask):
    pass


@dataclass(slots=True)
class BuildCoopTask(FarmTask):
    pass


@dataclass(slots=True)
class BuildPastureTask(FarmTask):
    pass


@dataclass(slots=True)
class PlaceAnimalTask(FarmTask):
    animal: Animal


# ============================================================
# Inventory
# ============================================================


@dataclass(slots=True)
class PickupTask(FarmTask):
    product: Product
    quantity: int = 1


@dataclass(slots=True)
class PlaceTask(FarmTask):
    product: Product
    quantity: int = 1


# ============================================================
# Market Tasks
# ============================================================


@dataclass(slots=True)
class MarketTask(Task):
    """
    Base class for all market operations.
    """


@dataclass(slots=True)
class BuySeedTask(MarketTask):
    crop: Crop
    quantity: int


@dataclass(slots=True)
class BuyAnimalTask(MarketTask):
    animal: Animal
    quantity: int = 1


@dataclass(slots=True)
class BuyProductTask(MarketTask):
    product: Product
    quantity: int


@dataclass(slots=True)
class SellTask(MarketTask):
    product: Product
    quantity: int


@dataclass(slots=True)
class HireTask(MarketTask):
    quantity: int = 1


@dataclass(slots=True)
class BuyLandTask(MarketTask):
    quadrant: Quadrant


# ============================================================
# Idle
# ============================================================


@dataclass(slots=True)
class WaitTask(Task):
    """
    Explicit idle task.
    """