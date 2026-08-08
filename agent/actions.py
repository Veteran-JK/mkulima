"""
agent/actions.py

Utilities for constructing valid Kaggriculture actions.

The planner should never build raw action lists directly.
Instead, it should use the helper functions in this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias

from .constants import (
    Animal,
    Crop,
    Direction,
    MarketAction,
    Product,
    Quadrant,
    WorkerAction,
)

# ============================================================
# Type Aliases
# ============================================================

from typing import TypeAlias

WorkerValue: TypeAlias = str | int
MarketValue: TypeAlias = str | int

WorkerOp: TypeAlias = list[WorkerValue]
MarketOp: TypeAlias = list[MarketValue]
# ============================================================
# Action Container
# ============================================================

@dataclass(slots=True)
class Actions:
    """
    Represents every action issued during a single turn.

    The Kaggle environment expects three independent action queues:
        - farmer
        - hands
        - market
    """

    farmer: WorkerOp = field(
        default_factory=lambda: [WorkerAction.PASS]
    )

    hands: list[WorkerOp] = field(default_factory=list)

    market: list[MarketOp] = field(default_factory=list)

    def to_dict(self) -> dict:
        """
        Convert the action container into the format expected by
        the Kaggle environment.
        """
        return {
            "farmer": self.farmer,
            "hands": self.hands,
            "market": self.market,
        }


# ============================================================
# Worker Actions
# ============================================================

def wait() -> WorkerOp:
    """Do nothing this turn."""
    return [WorkerAction.PASS]


def move(direction: Direction) -> WorkerOp:
    """Move one tile."""
    return [direction]


def pickup(item: Product, amount: int = 1) -> WorkerOp:
    """Pick up items from the current tile."""
    return [
        WorkerAction.PICKUP,
        item,
        amount,
    ]


def place(item: Product, amount: int = 1) -> WorkerOp:
    """Place items from inventory."""
    return [
        WorkerAction.PLACE,
        item,
        amount,
    ]


def plant(crop: Crop) -> WorkerOp:
    """Plant a crop."""
    return [
        WorkerAction.PLANT,
        crop,
    ]


def water() -> WorkerOp:
    """Water the current crop."""
    return [WorkerAction.WATER]


def harvest() -> WorkerOp:
    """Harvest the current crop."""
    return [WorkerAction.HARVEST]


def fertilize() -> WorkerOp:
    """Apply fertilizer."""
    return [WorkerAction.FERTILIZE]


def feed() -> WorkerOp:
    """Feed the animal."""
    return [WorkerAction.FEED]


def care() -> WorkerOp:
    """Care for the animal."""
    return [WorkerAction.CARE]


def collect_fertilizer() -> WorkerOp:
    """Collect fertilizer from an animal structure."""
    return [WorkerAction.COLLECT_FERTILIZER]


def build_coop() -> WorkerOp:
    """Build a goose coop."""
    return [WorkerAction.BUILD_COOP]


def build_pasture() -> WorkerOp:
    """Build a pasture."""
    return [WorkerAction.BUILD_PASTURE]


def dig() -> WorkerOp:
    """
    Dig the current tile.

    Can remove:
        - weeds
        - plants
        - coops
        - pastures
    """
    return [WorkerAction.DIG]


# ============================================================
# Market Actions
# ============================================================

def buy_seed(
    crop: Crop,
    quantity: int,
) -> MarketOp:
    """Queue a seed purchase."""
    return [
        MarketAction.BUY_SEED,
        crop,
        quantity,
    ]


def buy_product(
    product: Product,
    quantity: int,
) -> MarketOp:
    """
    Queue a market product purchase.

    Currently only WHEAT and FERTILIZER are purchasable.
    """
    return [
        MarketAction.BUY_PRODUCT,
        product,
        quantity,
    ]


def buy_animal(
    animal: Animal,
    quantity: int = 1,
) -> MarketOp:
    """Purchase livestock."""
    return [
        MarketAction.BUY_ANIMAL,
        animal,
        quantity,
    ]


def sell(
    product: Product,
    quantity: int,
) -> MarketOp:
    """Queue a market sell order."""
    return [
        MarketAction.SELL,
        product,
        quantity,
    ]


def hire() -> MarketOp:
    """Hire one farm hand."""
    return [MarketAction.HIRE]


def buy_land(
    quadrant: Quadrant,
) -> MarketOp:
    """
    Purchase an adjacent farm quadrant.

    Example:
        buy_land("NE")
    """
    return [
        MarketAction.BUY_LAND,
        quadrant,
    ]