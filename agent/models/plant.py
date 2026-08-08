"""
agent/models/plant.py

Represents a crop growing on a farm tile.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Plant:
    """
    Represents a crop on the farm.

    Attributes
    ----------
    crop : str
        Crop type (WHEAT, CARROT, TOMATO, etc.).

    planted_day : int
        Day the crop was planted.

    watered_today : bool
        Whether the crop has been watered today.

    consecutive_unwatered : int
        Number of consecutive days without water.

    yield_units : int
        Harvestable units currently available.

    max_lifespan_step : int
        Step at which decay begins (-1 for ongoing crops).

    fertilized_until_day : int
        Last day fertilizer bonus applies (-1 if inactive).
    """

    kind: str
    crop: str
    planted_day: int
    watered_today: bool
    consecutive_unwatered: int
    yield_units: int
    max_lifespan_step: int
    fertilized_until_day: int

    @property
    def is_harvestable(self) -> bool:
        """Return True if produce is ready for collection."""
        return self.yield_units > 0

    @property
    def needs_water(self) -> bool:
        """Return True if the crop has not yet been watered today."""
        return not self.watered_today

    @property
    def is_fertilized(self) -> bool:
        """Return True if fertilizer is currently active."""
        return self.fertilized_until_day >= 0

    def __repr__(self) -> str:
        return (
            f"Plant(crop={self.crop}, "
            f"yield={self.yield_units}, "
            f"watered={self.watered_today})"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Plant":
        """
        Create a Plant from a raw observation dictionary.
        """
        return cls(
            kind=data["kind"],
            crop=data["crop"],
            planted_day=data["planted_day"],
            watered_today=data["watered_today"],
            consecutive_unwatered=data["consecutive_unwatered"],
            yield_units=data["yield_units"],
            max_lifespan_step=data["max_lifespan_step"],
            fertilized_until_day=data["fertilized_until_day"],
        )