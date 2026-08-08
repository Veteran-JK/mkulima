"""
agent/models/unit.py

Represents the farmer or a hired farm hand.
"""

from __future__ import annotations

from dataclasses import dataclass

from .position import Position


@dataclass(slots=True)
class Unit:
    """
    Represents a worker on the farm.
    """

    position: Position

    is_farmer: bool = False

    def distance_to(self, other: Position) -> int:
        """
        Manhattan distance to another position.
        """
        return self.position.distance_to(other)

    def __repr__(self) -> str:
        role = "Farmer" if self.is_farmer else "FarmHand"
        return f"{role}(position={self.position})"

    @classmethod
    def from_position(
        cls,
        position: list[int],
        *,
        is_farmer: bool,
    ) -> "Unit":
        """
        Create a worker from the observation position.
        """
        return cls(
            position=Position(
                x=position[0],
                y=position[1],
            ),
            is_farmer=is_farmer,
        )