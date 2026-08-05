KNOWLEDGE BASE 

FACTS
------
- Season = 30 days
- Day = 24 turns
- Total turns = 720
- One action per worker per turn
- Market supply for seeds and animals is unlimited
- Winner determined by bank balance only

RULES
------
Plants
- Require watering once per day
- First yield only after minimum growth period
- Fertilizer doubles yield bonus for next 3 days

Animals
- Require feeding once per day
- Must be cared for
- Production depends on accumulated care bonus
...

CONSTRAINTS

Money

Actions

Movement

Farm size

Inventory

Shed capacity

Worker availability

Daily time (24 turns)


REQUIREMENTS

REQ-001
The agent must complete all 720 turns.

REQ-002
The agent must keep all living assets alive.

REQ-003
The agent must avoid wasting actions.

REQ-004
The agent must convert inventory into cash before the season ends.

REQ-005
The agent must adapt to changing market prices.

REQ-006
The agent must schedule work across available workers.

REQ-007
The agent must manage cash flow to avoid being unable to invest.

REQ-008
The agent must make decisions using only the current observation.


Observation Format
The top-level observation passed to each agent:

{
  "player": int,           # 0 or 1
  "day":    int,           # 0-indexed in-game day
  "hour":   int,           # 0-indexed turn within the day
  "farms":  [farm, farm],  # public per-player state, indexed by player id (shared)
  "market": {              # shared
    "inventory": { "WHEAT": int, "CARROT": int, ... },
    "prices":    { "WHEAT": int, "CARROT": int, ... },
  },
  "town": {                # shared
    "unlocked_shops": ["BAKERY", ...],
  },
  "private": {             # this player only; opponent's private state is not visible
    "shed":        { "WHEAT": int, "GOOSE": int, "FERTILIZER": int, ... },
    "seeds":       { "WHEAT": int, "CARROT": int, ... },
    "inventories": [farmer_inv, hand_inv, ...],  # [0] is the main farmer
  },
}
Each farm dict (public, visible to both players):

{
  "money":              float,
  "tiles":              [[tile, ...], ...],   # tiles[y][x]
  "farmer":             [x, y],
  "hands":              [[x, y], ...],         # hired hands for the current day
  "unlocked_quadrants": ["NW", ...],          # subset of {"NW","NE","SW","SE"}
  "hires_today":        int,                  # used to price the next HIRE
}
A tile is one of:

None — empty unlocked tile
"LOCKED" — tile in a quadrant the player has not yet bought
a plant dict:
  {
    "kind":                 "PLANT",
    "crop":                 "WHEAT" | "CARROT" | "TOMATO" | "STRAWBERRY" | "MELON",
    "planted_day":          int,
    "watered_today":        bool,   # reset to False each end-of-day
    "consecutive_unwatered": int,   # 2+ → tile turns to a weed
    "yield_units":          int,    # units currently harvestable
    "max_lifespan_step":    int,    # step at which decay begins; -1 for ongoing crops
    "fertilized_until_day": int,    # last day fertilizer bonus applies; -1 if none
  }
a weed dict: {"kind": "WEED"}
an animal structure dict (coop/pasture, optionally occupied):
  {
    "kind":                 "COOP" | "PASTURE",
    "animal":               "GOOSE" | "COW" | "SHEEP" | None,  # None until PLACEd
    "placed_day":           int,
    "yield_units":          int,
    "fed_today":            bool,
    "consecutive_unfed":    int,    # 2+ → animal escapes
    "cared_today":          bool,
    "fertilizer_available": bool,   # set after CARE; cleared by COLLECT_FERTILIZER
    "pending_care_bonus":   int,    # banked CARE bonus, applied on the next yield tick