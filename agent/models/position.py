"""
agent/models/position.py

Represents a position on the farm grid.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """
    Immutable position on the farm grid.
    """

    x: int
    y: int

    def distance_to(self, other: "Position") -> int:
        """
        Return the Manhattan distance to another position.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self) -> tuple["Position", ...]:
        """
        Return orthogonally adjacent positions in
        North, East, South, West order.
        """
        return (
            Position(self.x, self.y - 1),  # North
            Position(self.x + 1, self.y),  # East
            Position(self.x, self.y + 1),  # South
            Position(self.x - 1, self.y),  # West
        )

    def __iter__(self):
        """
        Allows:
            x, y = position
        """
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"