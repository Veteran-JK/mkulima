"""
agent/models/animal.py

Represents an animal structure (coop or pasture) occupying a farm tile.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnimalStructure:
    """
    Represents a livestock structure on the farm.

    Attributes
    ----------
    kind : str
        "COOP" or "PASTURE".

    animal : str | None
        Animal currently occupying the structure.

    placed_day : int
        Day the structure was placed.

    yield_units : int
        Harvestable units currently available.

    fed_today : bool
        Whether the animal has been fed today.

    consecutive_unfed : int
        Consecutive days without feeding.

    cared_today : bool
        Whether the animal has been cared for today.

    fertilizer_available : bool
        Whether fertilizer can be collected.

    pending_care_bonus : int
        Banked care bonus applied on the next production cycle.
    """

    kind: str
    animal: str | None
    placed_day: int
    yield_units: int
    fed_today: bool
    consecutive_unfed: int
    cared_today: bool
    fertilizer_available: bool
    pending_care_bonus: int

    @property
    def has_animal(self) -> bool:
        """True if an animal occupies the structure."""
        return self.animal is not None

    @property
    def needs_food(self) -> bool:
        """True if today's feeding has not been completed."""
        return self.has_animal and not self.fed_today

    @property
    def needs_care(self) -> bool:
        """True if today's care has not been completed."""
        return self.has_animal and not self.cared_today

    @property
    def has_yield(self) -> bool:
        """True if produce is available."""
        return self.yield_units > 0

    @property
    def has_fertilizer(self) -> bool:
        """True if fertilizer can be collected."""
        return self.fertilizer_available

    def __repr__(self) -> str:
        return (
            f"AnimalStructure("
            f"kind={self.kind}, "
            f"animal={self.animal}, "
            f"yield={self.yield_units})"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "AnimalStructure":
        """
        Create an AnimalStructure from a raw observation dictionary.
        """
        return cls(
            kind=data["kind"],
            animal=data["animal"],
            placed_day=data["placed_day"],
            yield_units=data["yield_units"],
            fed_today=data["fed_today"],
            consecutive_unfed=data["consecutive_unfed"],
            cared_today=data["cared_today"],
            fertilizer_available=data["fertilizer_available"],
            pending_care_bonus=data["pending_care_bonus"],
        )