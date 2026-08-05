# Kaggriculture — Knowledge Base

Condensed, agent-development-oriented reference distilled from `README.md` and
`AGENTS.md`. This is the "facts" doc — mechanics, numbers, formats. Strategy
and code architecture live in `DESIGN.md`.

---

## 1. Season Shape

- `turnsPerDay = 24`, `days = 30` → `episodeSteps = 720` turns total (defaults).
- Turn 0 = day 0, hour 0. `day = step // turnsPerDay`, `hour = step % turnsPerDay`.
- Win = most money in bank at end. Unsold inventory doesn't count. Ties possible.

## 2. Farm & Units

- Grid `boardSize × boardSize` (default 10×10), 4 quadrants of 5×5: `NW` (free/start),
  `NE`, `SW`, `SE` (buy via `BUY_LAND` for $1k / $2k / $4k, in that order).
- `startingMoney = 3000`.
- One main **farmer** + up to N **farm hands** hired per day.
  - Hire cost: `farmHandCostMult * fib(n)`, `n` = hires already made *today*.
    Default mult = 1 → costs `1, 1, 2, 3, 5, 8, 13, 21, ...`. Resets daily.
  - Hands spawn orthogonally adjacent to shed (NWSE preference / least-occupied tiebreak),
    act independently each turn, **disappear at end of day** (re-hire needed).
  - Both farmer and hands act via the same op set; farmer/hands can share a tile.
- Shed-adjacent tiles: `(4,4)`, `(4,5)`, `(5,4)`, `(5,5)` (the 2×2 center — shed itself
  is not a `tiles` entry).

## 3. Object Types (crops & animals)

| Type | Yield type | Seed cost | Base price | 1st yield | Max yield day | Subsequent | Max yield/plant | Action cost | Max yield/tile/day |
|---|---|---|---|---|---|---|---|---|---|
| Wheat | One-time | 10 | 25 | day 2 | day 4 | none | 6 | 1 | 1.5 |
| Carrot | One-time | 20 | 35 | day 2 | day 3 | none | 4 | 1 | 1.333 |
| Tomato | Ongoing | 50 | 60 | day 8 | NA | every day | 4/cycle | 1 | 4 |
| Strawberry | Ongoing | 100 | 120 | day 10 | NA | every other day | 4/cycle | 1 | 2 |
| Melon | One-time | 80 | 250 | day 10 | day 12 | none | 6 | 1 | 0.5 |
| Goose→Egg | Ongoing | 300 | 50 | day 4 | NA | every day | 4/cycle | 1 + build coop | 2 |
| Cow→Milk | Ongoing | 400 | 160 | day 8 | NA | every 2 days | 6/cycle | 1 + build pasture | 1 |
| Sheep→Wool | Ongoing | 500 | 200 | day 6 | NA | every 3 days | 6/cycle | 1 + build pasture | 0.67 |
| Fertilizer | — | 100 | — (buy 100, see price table) | — | — | — | — | 1 | — |

Wheat doubles as **animal feed** — factor this into any animal strategy.

## 4. Watering / Feeding (survival)

- Every plant needs `WATER` and every animal needs `FEED` **once per day** (extra
  same-day calls are no-ops).
- **Two consecutive missed days → plant becomes WEED / animal escapes (unrecoverable)**.
- Planting day counts as day 1 of the "unwatered" clock — i.e. you must water same-day
  or next-day, not skip straight to day 2.

## 5. Yield Mechanics

### One-time crops (Wheat, Carrot, Melon)
- Bonus watering window starts at `ceil(max_yield_day / 2)`.
- Watering during the window: **+1 unit/day** to total harvestable yield.
- `FERTILIZE`: doubles the per-day bonus to **+2/day** for the next 3 days
  (bonus still requires that day also be watered — basic needs first).
- Harvest yields whatever `yield_units` has accumulated; removes plant from map
  (no regrowth).

### Ongoing crops (Tomato, Strawberry) & Animals (Goose, Cow, Sheep)
- Fixed production schedule (see "Subsequent" column above / animal cadence).
- Base yield on a scheduled production tick = 1.
- Crops: doubled to 2 if fertilized **and** watered that same day.
- Animals: see CARE mechanic below (banked bonus instead of fertilize/water combo).

### Animal CARE mechanic
- `CARE` once/day (no-op if already cared today).
- End of day: if fed **and** cared that day → `pending_care_bonus += 2`. Unfed days
  bank nothing.
- On a scheduled production day: if fed, yield = `1 + pending_care_bonus`, bank resets
  to 0. If unfed on the production day, **no yield produced**, bank still resets.
- `pending_care_bonus` is implicitly capped by the animal's `max_held` (cap on
  unharvested `yield_units` sitting on the tile — not a lifetime cap; animals produce
  indefinitely while fed).

### Decay (after max lifespan)
- One-time crops: lifespan ends 1 day after `max_yield_day`.
- Ongoing crops: lifespan ends 1 day after cumulative production count hits `max_yield`
  (i.e., enough scheduled ticks have fired, harvested or not).
- Past lifespan: `yield_units` drops by 1 **every other turn** until 0 → tile becomes WEED.

### Fertilizer collection
- `COLLECT_FERTILIZER`: animals make 1 fertilizer available per surviving animal at
  end-of-day refresh; collecting consumes that day's stock, next batch available after
  the following end-of-day refresh.

## 6. Weeds & Digging

- Every empty **unlocked** tile: `weedSpawnChance` (default 0.005) chance/day of
  spawning a weed at end-of-day.
- `DIG` removes: a plant (no yield), a weed, or an **empty** coop/pasture (occupied
  structures can't be dug — must remove/lose the animal first, which isn't directly
  possible except via escape from neglect).

## 7. Shed & Inventory

- Shed cap: 100 non-seed items. Overflow at end-of-day drop (or mid-day `PLACE`) is
  **discarded**, not held anywhere else.
- Seeds: separate uncapped slot, never enter the shed, `PLANT` consumes directly.
- Farmer/hands spawn at shed at start of day; **all unit inventories dump into shed at
  end of day** (subject to the 100 cap — overflow lost).
- `PICKUP <item> [n]` — from shed into active unit's inventory (shed-adjacent required).
- `DROP` — shed-adjacent, dumps entire inventory into shed.
- `PLACE <item> [n]` — dual purpose:
  - On an unoccupied matching structure (GOOSE→coop, COW/SHEEP→pasture): places one
    animal (n ignored).
  - Shed-adjacent: moves up to n of item into shed (same as partial DROP).

## 8. Actions Reference

One action per unit per turn. Format:

```py
{
  "farmer": [op, ...args],
  "hands":  [[op, ...args], ...],   # one entry per hand, in hands order
  "market": [[op, ...args], ...],   # ≤ maxMarketOrdersPerTurn, extras dropped silently
}
```

**Movement**: `NORTH`, `SOUTH`, `EAST`, `WEST`, `PASS`. Locked tiles are passable
(crossable) but not actionable.

**Shed/inventory**: `PICKUP <item> [n]`, `PLACE <item> [n]`, `DROP`.

**Plants**: `PLANT <crop>`, `WATER`, `HARVEST`, `FERTILIZE`.
- Simultaneous over-planting guard: if N units all try to `PLANT` the same crop this
  turn but you only have seeds for fewer, **none** are planted.

**Animals**: `BUILD_COOP`, `BUILD_PASTURE`, `FEED`, `COLLECT_FERTILIZER`, `CARE`,
`HARVEST` (collects eggs/milk/wool).

**Terrain**: `DIG`.

**Market** (list, ordered, capped at `maxMarketOrdersPerTurn`, default 10):
`["BUY_SEED", crop, n]`, `["BUY_PRODUCT", item, n]` (WHEAT & FERTILIZER only),
`["BUY_ANIMAL", animal, n]`, `["SELL", item, n]`, `["HIRE"]`, `["BUY_LAND"]`.

All invalid actions are **silent no-ops** — no penalty, no error, just nothing happens.
This matters for defensive coding: don't assume failure will be visible.

## 9. Market Mechanics

- Every product + fertilizer starts with market inventory `I0 = 10,000` (per side,
  shared across both players).
- Price formula:
  ```
  price(inv) = base + sign · amp · f(|inv − I0|)
  sign = +1 if inv < I0 (scarcity → price up), -1 if inv > I0 (glut → price down)
  amp = target · base / f(T)     (derived)
  f ∈ {linear, sq, sqrt, log}    (independently chosen per side of I0)
  ```
  Floored at $1, rounded to nearest dollar.
- `T` = single-5×5-field production capacity over 24 days at optimal watering, no
  fertilizer (animal `T` pre-discounted 30% for wheat-feed overhead).
- Orders (buy or sell) process **one unit at a time, concurrently across both players**
  — e.g. both `SELL CARROT 10` ⇒ take turns unit-by-unit, price can shift mid-order.
- At the $1 floor, sells still execute but **don't add inventory** — keeps the floor
  responsive to subsequent buys.
- Only `WHEAT` and `FERTILIZER` are buyable via `BUY_PRODUCT`; everything is sellable.
- Buy price quoted at post-buy inventory; sell price quoted at pre-sell inventory ⇒
  an immediate buy+sell of the same qty nets exactly $0 (no-arb identity, useful as a
  sanity check when reasoning about the formula).
- If money runs out mid buy-order, the order just stops (partial fill).

### Price Function Table (defaults)

| Resource | Base | I0 | T | Below func | Below tgt | Above func | Above tgt | P(I0−T) | P(I0+T) | P(I0+2T) |
|---|---|---|---|---|---|---|---|---|---|---|
| Wheat | 25 | 10,000 | 400 | sqrt | 0.80 | log | 0.20 | $45 | $20 | $19 |
| Carrot | 35 | 10,000 | 450 | log | 0.20 | sqrt | 0.70 | $42 | $10 | $1 |
| Tomato | 60 | 10,000 | 200 | linear | 0.40 | sqrt | 0.60 | $84 | $24 | $9 |
| Strawberry | 120 | 10,000 | 100 | sqrt | 0.70 | linear | 1.60 | $204 | $1 | $1 |
| Melon | 250 | 10,000 | 300 | log | 0.20 | sq | 3.60 | $300 | $1 | $1 |
| Egg | 50 | 10,000 | 332 | linear | 0.40 | log | 0.20 | $70 | $40 | $39 |
| Milk | 160 | 10,000 | 122 | sqrt | 0.60 | linear | 1.60 | $256 | $1 | $1 |
| Wool | 200 | 10,000 | 105 | log | 0.20 | sq | 3.20 | $240 | $1 | $1 |
| Fertilizer | 100 | 10,000 | 200 | linear | 0.40 | linear | 0.40 | $140 | $60 | $20 |

**Takeaways**: Wheat/carrot are staples — they absorb gluts gently but wheat panics
hard on scarcity (you'll need it for feed, so scarcity self-inflicted by heavy animal
use is a real risk). Premium goods (strawberry, melon, milk, wool — base > $100, high
`above_target`) crash to the $1 floor fast on oversupply → **sell these in small,
timed batches, not dumps**, and expect diminishing returns from scaling any one
premium good too far.

## 10. Town Demand (passive market drain — works in your favor as a seller)

- Town center: demands 1 of every non-fertilizer product every `townCenterSellInterval`
  turns (default 12) → scales to 2× after day 10, 4× after day 20.
- Additional shops unlock every `townShopUnlockInterval` days (default 3), random
  selection from remaining pool, permanent once unlocked.
- Each unlocked shop consumes 1 of every product it demands every
  `townShopSellInterval` turns (default 4); **single-product shops consume 2×**.

| Shop | Demands |
|---|---|
| Bakery | eggs, wheat |
| Pizza Shop | milk, tomatoes, wheat |
| Brunch Spot | eggs, wheat, strawberries |
| Yarn Store | wool (2×) |
| Ice Cream Shop | strawberries, milk, wheat |
| Pet Cafe | carrots (2×) |
| Smoothie Shop | strawberries, milk |
| Farmers Market | wheat, carrots, tomatoes, strawberries |

Town consumption is *not* a sale you make — it just drains market inventory, which
props up prices for your own future sells. Worth modeling passively; not something
you interact with directly.

## 11. Turn Processing Order (per step)

1. Action validation
2. Player actions recorded (simultaneous)
3. Market actions processed in order, by player, concurrently unit-by-unit
4. Town buy actions (drain inventory)
5. Observation update:
   - Day refresh (if applicable): plant/animal condition update, fed/watered flags reset
   - Market refresh: price recompute from prior-turn sells
   - Income update: bank adjusted for buys/sells
   - Farm update: harvested plants cleared, consumed inventory removed, new plants/animals added

## 12. Observation Format (cheat sheet)

```py
obs = {
  "player": 0 | 1,
  "step": int, "day": int, "hour": int,
  "farms": [farm0, farm1],   # public, both visible
  "market": {"inventory": {...}, "prices": {...}},
  "town": {"unlocked_shops": [...]},
  "private": {"shed": {...}, "seeds": {...}, "inventories": [...]},  # own only
}

farm = {
  "money": float,
  "tiles": [[tile,...],...],           # tiles[y][x]
  "farmer": [x, y],
  "hands": [[x,y],...],
  "unlocked_quadrants": [...],
  "hires_today": int,
}

# tile is one of: None | "LOCKED" | plant dict | weed dict | structure dict
plant = {"kind":"PLANT","crop":str,"planted_day":int,"watered_today":bool,
         "consecutive_unwatered":int,"yield_units":int,
         "max_lifespan_step":int,"fertilized_until_day":int}
weed = {"kind":"WEED"}
structure = {"kind":"COOP"|"PASTURE","animal":str|None,"placed_day":int,
             "yield_units":int,"fed_today":bool,"consecutive_unfed":int,
             "cared_today":bool,"fertilizer_available":bool,"pending_care_bonus":int}
```

## 13. Configuration Defaults

| Param | Default | Notes |
|---|---|---|
| episodeSteps | 720 | 24×30 |
| boardSize | 10 | 4× 5×5 quadrants |
| startingMoney | 3000 | |
| maxMarketOrdersPerTurn | 10 | extras silently dropped |
| turnsPerDay | 24 | |
| shedCapacity | 100 | excl. seeds |
| weedSpawnChance | 0.005 | per empty unlocked tile/day |
| townShopUnlockInterval | 3 days | |
| townShopSellInterval | 4 turns | |
| townCenterSellInterval | 12 turns | scales 2×/4× at day 10/20 |
| seed | null | deterministic episodes if set |

Per-resource market params overridable at episode creation via
`env.configuration["marketParams"]` (sparse overrides: `base`, `I0`, `T`,
`below_func`, `below_target`, `above_func`, `above_target`).

## 14. Open Questions to Verify Empirically (before relying on them in DESIGN.md)

These aren't fully pinned down by the docs and are worth a quick local-sim check:

- Exact `T` "animal totals pre-discounted 30%" — confirm whether this changes
  effective per-animal-per-day yield expectations vs. the raw cadence numbers.
- Whether `HARVEST` on an ongoing crop/animal before a scheduled tick is a no-op or
  invalid (docs imply yield only exists at `yield_units > 0`, so likely just no-op
  with 0 yield).
- Behavior of `BUY_LAND` order enforcement (must NE→SW→SE, or any order once
  affordable?) — README doesn't state an order constraint explicitly beyond cost tiers.