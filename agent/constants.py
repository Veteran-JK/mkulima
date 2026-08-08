"""
agent/constants.py

Shared constants and enumerations for the Kaggriculture agent.

This module centralizes game vocabulary and removes magic strings and
numbers from the rest of the codebase.
"""

from __future__ import annotations

from enum import StrEnum

# ============================================================
# Game Defaults
# ============================================================

BOARD_SIZE = 10
QUADRANT_SIZE = 5

TURNS_PER_DAY = 24
DAYS_PER_SEASON = 30
TOTAL_TURNS = TURNS_PER_DAY * DAYS_PER_SEASON

STARTING_MONEY = 3000

SHED_CAPACITY = 100

MAX_MARKET_ORDERS = 10


# ============================================================
# Directions
# ============================================================

class Direction(StrEnum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


# ============================================================
# Crops
# ============================================================

class Crop(StrEnum):
    WHEAT = "WHEAT"
    CARROT = "CARROT"
    TOMATO = "TOMATO"
    STRAWBERRY = "STRAWBERRY"
    MELON = "MELON"


# ============================================================
# Animals
# ============================================================

class Animal(StrEnum):
    GOOSE = "GOOSE"
    COW = "COW"
    SHEEP = "SHEEP"


# ============================================================
# Products
# ============================================================

class Product(StrEnum):
    WHEAT = "WHEAT"
    CARROT = "CARROT"
    TOMATO = "TOMATO"
    STRAWBERRY = "STRAWBERRY"
    MELON = "MELON"

    EGG = "EGG"
    MILK = "MILK"
    WOOL = "WOOL"

    FERTILIZER = "FERTILIZER"


# ============================================================
# Structures
# ============================================================

class Structure(StrEnum):
    COOP = "COOP"
    PASTURE = "PASTURE"


# ============================================================
# Tile Types
# ============================================================

class TileKind(StrEnum):
    PLANT = "PLANT"
    WEED = "WEED"

    COOP = "COOP"
    PASTURE = "PASTURE"

    LOCKED = "LOCKED"


# ============================================================
# Farm Quadrants
# ============================================================

class Quadrant(StrEnum):
    NW = "NW"
    NE = "NE"
    SW = "SW"
    SE = "SE"


# ============================================================
# Worker Actions
# ============================================================

class WorkerAction(StrEnum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

    PASS = "PASS"

    PICKUP = "PICKUP"
    PLACE = "PLACE"

    PLANT = "PLANT"
    WATER = "WATER"
    HARVEST = "HARVEST"
    FERTILIZE = "FERTILIZE"

    BUILD_COOP = "BUILD_COOP"
    BUILD_PASTURE = "BUILD_PASTURE"

    FEED = "FEED"
    CARE = "CARE"

    COLLECT_FERTILIZER = "COLLECT_FERTILIZER"

    DIG = "DIG"


# ============================================================
# Market Actions
# ============================================================

class MarketAction(StrEnum):
    BUY_SEED = "BUY_SEED"

    BUY_PRODUCT = "BUY_PRODUCT"

    BUY_ANIMAL = "BUY_ANIMAL"

    SELL = "SELL"

    HIRE = "HIRE"

    BUY_LAND = "BUY_LAND"