"""
agent/pathing.py

Generic pathfinding utilities.

This module contains reusable navigation algorithms.
It deliberately contains no farming, market, or strategy logic.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable

from agent.constants import Direction
from agent.models.position import Position
from agent.models.tile import Tile


# ============================================================
# Distance Utilities
# ============================================================


def manhattan_distance(
    a: Position,
    b: Position,
) -> int:
    """
    Manhattan distance between two positions.
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def adjacent(
    a: Position,
    b: Position,
) -> bool:
    """
    True if positions are orthogonally adjacent.
    """
    return manhattan_distance(a, b) == 1


# ============================================================
# Neighbor Generation
# ============================================================


def neighbors(
    position: Position,
    board_size: int,
) -> list[Position]:
    """
    Return valid neighboring positions.
    """

    result: list[Position] = []

    if position.y > 0:
        result.append(Position(position.x, position.y - 1))

    if position.y < board_size - 1:
        result.append(Position(position.x, position.y + 1))

    if position.x > 0:
        result.append(Position(position.x - 1, position.y))

    if position.x < board_size - 1:
        result.append(Position(position.x + 1, position.y))

    return result


# ============================================================
# Direction Utilities
# ============================================================


def direction_to(
    current: Position,
    target: Position,
) -> Direction:
    """
    Return the direction from one adjacent position to another.
    """

    dx = target.x - current.x
    dy = target.y - current.y

    if dx == 1 and dy == 0:
        return Direction.EAST

    if dx == -1 and dy == 0:
        return Direction.WEST

    if dy == 1 and dx == 0:
        return Direction.SOUTH

    if dy == -1 and dx == 0:
        return Direction.NORTH

    raise ValueError(
        "Positions must be orthogonally adjacent."
    )


# ============================================================
# Walkability
# ============================================================


def is_walkable(tile: Tile) -> bool:
    """
    Determine whether a tile can be traversed.

    Currently every unlocked tile is considered walkable.
    This can be refined later if movement rules become
    more restrictive.
    """
    return tile.unlocked


# ============================================================
# Path Reconstruction
# ============================================================


def reconstruct_path(
    goal: Position,
    came_from: dict[Position, Position | None],
) -> list[Position]:
    """
    Reconstruct a shortest path produced by BFS.
    """

    path: list[Position] = []

    current: Position | None = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path


# ============================================================
# Breadth-First Search
# ============================================================


def bfs(
    start: Position,
    goal: Position,
    tile_at: Callable[[int, int], Tile],
    board_size: int,
) -> list[Position]:
    """
    Compute a shortest path using Breadth-First Search.

    Returns an empty list if no path exists.
    """

    queue = deque([start])

    came_from: dict[Position, Position | None] = {
        start: None,
    }

    while queue:

        current = queue.popleft()

        if current == goal:
            break

        for nxt in neighbors(current, board_size):

            if nxt in came_from:
                continue

            tile = tile_at(
                nxt.x,
                nxt.y,
            )

            if not is_walkable(tile):
                continue

            came_from[nxt] = current

            queue.append(nxt)

    if goal not in came_from:
        return []

    return reconstruct_path(
        goal,
        came_from,
    )


# ============================================================
# Navigation Helper
# ============================================================


def next_step(
    start: Position,
    goal: Position,
    tile_at: Callable[[int, int], Tile],
    board_size: int,
) -> Direction | None:
    """
    Return the first movement required to travel toward
    the goal.

    Returns None if already at the goal or if no path exists.
    """

    path = bfs(
        start=start,
        goal=goal,
        tile_at=tile_at,
        board_size=board_size,
    )

    if len(path) < 2:
        return None

    return direction_to(
        path[0],
        path[1],
    )