"""
agent/models/farm.py

Represents the public state of one player's farm.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .position import Position
from .tile import Tile
from .unit import Unit



@dataclass(slots=True)
class Farm:
    """
    Represents a player's farm.

    This model contains observable game state only.
    """

    money: float

    tiles: list[list[Tile]]

    farmer: Unit

    hands: list[Unit] = field(default_factory=list)

    unlocked_quadrants: set[str] = field(default_factory=set)

    hires_today: int = 0

    @property
    def width(self) -> int:
        """Width of the farm."""
        return len(self.tiles[0]) if self.tiles else 0

    @property
    def height(self) -> int:
        """Height of the farm."""
        return len(self.tiles)

    @property
    def workers(self) -> list[Unit]:
        """Return all workers."""
        return [self.farmer, *self.hands]

    def tile_at(self, position: Position) -> Tile:
        """
        Return the tile at a position.
        """
        return self.tiles[position.y][position.x]

    def in_bounds(self, position: Position) -> bool:
        """
        Check whether a position lies inside the farm.
        """
        return (
            0 <= position.x < self.width
            and 0 <= position.y < self.height
        )

    def is_unlocked(self, position: Position) -> bool:
        """
        Return whether a tile is unlocked.
        """
        return self.tile_at(position).unlocked

    def neighbors(self, position: Position) -> list[Tile]:
        """
        Return all orthogonally adjacent tiles within the farm.
        """
        adjacent: list[Tile] = []

        for neighbor in position.neighbors():
            if self.in_bounds(neighbor):
                adjacent.append(self.tile_at(neighbor))

        return adjacent

    def __repr__(self) -> str:
        return (
            f"Farm("
            f"money={self.money}, "
            f"size={self.width}x{self.height}, "
            f"workers={len(self.workers)}, "
            f"quadrants={sorted(self.unlocked_quadrants)})"
        )
    @classmethod
    def from_dict(cls, data: dict) -> "Farm":
        """
        Create a Farm from a raw observation dictionary.
        """

        tiles: list[list[Tile]] = []

        for y, row in enumerate(data["tiles"]):

            tile_row: list[Tile] = []

            for x, tile in enumerate(row):

                tile_row.append(
                    Tile.from_dict(
                        tile,
                        x=x,
                        y=y,
                    )
                )

            tiles.append(tile_row)

        farmer = Unit.from_position(
            data["farmer"],
            is_farmer=True,
        )

        hands = [
            Unit.from_position(
                hand,
                is_farmer=False,
            )
            for hand in data["hands"]
        ]

        return cls(
            money=data["money"],
            tiles=tiles,
            farmer=farmer,
            hands=hands,
            unlocked_quadrants=set(
                data["unlocked_quadrants"]
            ),
            hires_today=data["hires_today"],
        )
