"""
agent/models/tile.py

Represents a single tile on the farm.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent.models.animal import AnimalStructure
from agent.models.plant import Plant
from agent.models.position import Position


@dataclass(slots=True)
class Tile:
    """
    Represents one square on the player's farm.
    """

    position: Position

    unlocked: bool

    occupant: Any | None = None

    @property
    def is_locked(self) -> bool:
        """Return True if this tile is locked."""
        return not self.unlocked

    @property
    def is_empty(self) -> bool:
        """Return True if the tile is unlocked and has no occupant."""
        return self.unlocked and self.occupant is None

    @property
    def has_plant(self) -> bool:
        """Return True if the tile contains a plant."""
        return (
            self.occupant is not None
            and getattr(self.occupant, "kind", None) == "PLANT"
        )

    @property
    def has_animal(self) -> bool:
        """Return True if the tile contains a livestock structure."""
        return (
            self.occupant is not None
            and getattr(self.occupant, "kind", None) in {"COOP", "PASTURE"}
        )

    @property
    def has_weed(self) -> bool:
        """Return True if the tile contains a weed."""
        return (
            self.occupant is not None
            and getattr(self.occupant, "kind", None) == "WEED"
        )

    def __repr__(self) -> str:
        occupant = (
            type(self.occupant).__name__
            if self.occupant is not None
            else "Empty"
        )

        return (
            f"Tile(position={self.position}, "
            f"unlocked={self.unlocked}, "
            f"occupant={occupant})"
        )

    @classmethod
    def from_dict(
        cls,
        data,
        *,
        x: int,
        y: int,
    ) -> "Tile":
        """
        Create a Tile from a raw observation tile.
        """

        position = Position(x=x, y=y)

        if data is None:
            return cls(
                position=position,
                unlocked=True,
            )

        if data == "LOCKED":
            return cls(
                position=position,
                unlocked=False,
            )

        kind = data["kind"]

        if kind == "PLANT":
            occupant = Plant.from_dict(data)

        elif kind in {"COOP", "PASTURE"}:
            occupant = AnimalStructure.from_dict(data)

        elif kind == "WEED":
            occupant = data

        else:
            raise ValueError(f"Unknown tile type: {kind}")

        return cls(
            position=position,
            unlocked=True,
            occupant=occupant,
        )