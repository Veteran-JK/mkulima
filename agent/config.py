"""
config.py

Configuration for the Mkulima Kaggriculture agent.

Only agent-specific configuration belongs here.
Game rules and constants belong in agent/constants.py.
"""

from __future__ import annotations

# ============================================================
# Debug Configuration
# ============================================================

DEBUG = False
LOG_ACTIONS = False
LOG_STRATEGY = False
LOG_PATHING = False
LOG_WORLD = False

# ============================================================
# Randomness
# ============================================================

RANDOM_SEED = 42

# ============================================================
# Planner Configuration
# ============================================================

MAX_PATH_LENGTH = 100

# ============================================================
# Strategy Configuration
# ============================================================

ENABLE_EMERGENCY_STRATEGY = True
ENABLE_OPENING_STRATEGY = True
ENABLE_FARMING_STRATEGY = True
ENABLE_LIVESTOCK_STRATEGY = True
ENABLE_MARKET_STRATEGY = True
ENABLE_ECONOMY_STRATEGY = True
ENABLE_EXPANSION_STRATEGY = True

# ============================================================
# Experimental Features
# ============================================================

USE_HEURISTICS = True
USE_MARKET_FORECAST = False
USE_DYNAMIC_PRIORITIES = False