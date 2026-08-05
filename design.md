# Kaggriculture — Agent Design

Companion to `KNOWLEDGE.md` (mechanics reference). This doc is the "how we build it"
plan: architecture, strategy phases, priorities, and a build/test roadmap. Treat it as
a living doc — update it as local sims reveal what actually works.

---

## 1. Design Goals

1. **Correctness first**: never issue an action that silently no-ops when a valid
   action was available (wasted turns are the main way a mediocre agent loses).
2. **Survive before optimize**: watering/feeding logic must be bulletproof before any
   yield-maximization logic runs — losing a plant/animal to neglect is a much bigger
   loss than a suboptimal sale price.
3. **Modular decision layers** so strategy can be tuned/replaced independently of the
   observation-parsing and action-emitting plumbing.
4. **Deterministic, testable core** — the market/yield math should be unit-testable
   against the formulas in `KNOWLEDGE.md` without spinning up a full episode.

## 2. Proposed File Structure

```
main.py              # entry point: agent(obs) -> action dict (required at submission root)
state.py             # parses obs into typed, convenient structures
planner.py           # top-level turn loop: decides one op per unit + market list
strategy/
  farming.py         # per-tile crop lifecycle decisions (plant/water/fertilize/harvest/dig)
  animals.py         # coop/pasture lifecycle decisions (feed/care/collect/harvest)
  market.py          # buy/sell decisions, price-aware batching
  expansion.py        # BUY_LAND / HIRE timing decisions
pathing.py            # movement: shortest path from unit pos -> target tile
config.py             # tunable constants (thresholds, priorities) kept out of logic
test_local.py         # local harness using kaggle_environments to run + score agents
```

Single-file submission (`main.py`) can just inline everything if the multi-file tar.gz
route feels like overkill early on — but developing across modules and only
concatenating/bundling at submission time keeps iteration sane. Recommend using the
tar.gz path (`AGENTS.md` supports it) from day one so this split is free.

## 3. State Layer (`state.py`)

Wrap the raw `obs` dict once per turn into something easier to reason about:

- `Farm` — money, tiles (with helper `tile_at(x,y)`), farmer pos, hands, unlocked
  quadrants, hires_today.
- `Tile` classification helper: `EMPTY | LOCKED | WEED | PLANT | COOP | PASTURE`.
- `Unit` — position + inventory (index-aligned with `hands`), with a `is_hand` flag.
- `Market` — inventory + prices, plus a `projected_sell_value(item, qty)` helper that
  simulates the unit-at-a-time price walk from `KNOWLEDGE.md §9` so selling decisions
  can compare "sell now" vs. "hold" without re-deriving the formula ad hoc.

Keep this layer **read-only / pure** — no mutation, no side effects — so it can be
reused directly in unit tests against hand-built fixture observations.

## 4. Planner Loop (`planner.py`)

Per turn, for the farmer and each hand independently:

1. **Survival check** — is there a plant/animal on my current tile (or reachable this
   turn) at risk of a second consecutive missed water/feed? If yes, prioritize that
   over everything else. This is the only "interrupt" tier.
2. **Local action** — if standing on an actionable tile, decide the single best op
   for *this* tile (see `strategy/farming.py` / `strategy/animals.py`).
3. **Movement fallback** — no useful local action → pathfind toward the
   highest-priority target tile from a ranked worklist (see §6).
4. **Shed logic** — inventory management (`PICKUP`/`PLACE`/`DROP`) folded into the
   same priority scan: full inventory near cap → route to shed; empty-handed with
   seeds needed at a target tile is *not* a thing (seeds auto-apply via `PLANT`), so
   this is really only for harvested produce and animals-in-transit.

Then separately, once per turn: build the **market order list** (`strategy/market.py`)
and evaluate **expansion** (`strategy/expansion.py`) — these don't depend on unit
positions and can run after the movement/action decisions.

## 5. Strategy Phases

Recommend an explicit game-phase signal (`day` thresholds, tune empirically) rather
than one static policy, since the profitable move set changes a lot over 30 days:

| Phase | Days (approx) | Focus |
|---|---|---|
| **Bootstrap** | 0–3 | Wheat/carrot loop only (cheap, fast payback). Build cash buffer. No hires yet unless clearly cash-positive same-day. |
| **Ramp** | 3–10 | First `BUY_LAND` once cash supports it without starving the wheat loop. Start ongoing crops (tomato) — 8-day lead time means day 3–5 is the latest sensible start to have income by mid-game. Consider first coop (goose, 4-day lead, cheapest animal). |
| **Scale-up** | 10–20 | Second/third quadrant, hands hired opportunistically, pasture animals (cow/sheep) if wheat-feed supply chain is solid, melon plots (long lead but big payoff, low max-yield/tile so needs many tiles). |
| **Wind-down** | 20–30, esp. last 5 | Stop starting anything with a lead time that won't pay off before season end (e.g. don't plant melon after ~day 18; don't buy land after ~day 26). Shift to liquidating standing inventory — start batching sells earlier for premium goods since dumping late crashes price into the floor with no time to recover. |

The exact day cutoffs above are first-pass estimates from the yield-time table — treat
them as tunable constants (`config.py`), and validate/adjust via local sim scoring
rather than trusting the numbers as designed.

## 6. Tile Prioritization (worklist ranking)

For movement targeting, rank actionable tiles by an estimated **$/turn-of-attention**
heuristic rather than raw yield, since attention (unit-turns) is the scarcer resource
once you have >1 tile in play:

```
score(tile) ≈ expected_marginal_revenue(action) / turns_to_reach(unit, tile)
```

Where `expected_marginal_revenue` accounts for:
- Water/fertilize actions on crops in their bonus window (yield delta × current
  projected sell price for that crop).
- Harvest actions (immediate realized yield × projected sell price, discounted for
  expected price impact of adding to shed/eventual sale).
- Feed/care on animals close to a scheduled production tick (banked-bonus payoff).
- Weed clearing (opportunity cost of a blocked tile) and new-plant tiles (upfront seed
  cost amortized over the crop's expected lifetime revenue).

This is the piece most worth prototyping in isolation with a spreadsheet or quick
script before wiring into the full planner — get the relative ordering right on paper
first.

## 7. Market Strategy (`strategy/market.py`)

- **Selling**: batch, don't dump. Use `Market.projected_sell_value` to find the
  quantity at which marginal price for a batch drops below a floor threshold
  (tunable per resource — premium goods need a tighter cap given `above_target` > 1
  for strawberry/melon/wool per `KNOWLEDGE.md §9`), and split remainder across turns.
- **Buying wheat for feed**: model expected daily wheat consumption from animal count
  and keep a rolling buffer via `BUY_PRODUCT` rather than reactive last-minute buys
  (scarcity pricing on wheat is the steepest `below_target` in the table — 0.80 — so
  panic-buying wheat is expensive).
- **Fertilizer**: buy proactively ahead of fertilize-heavy pushes (e.g. right before
  a one-time crop enters its bonus window) rather than same-turn.
- Respect `maxMarketOrdersPerTurn` (default 10) — prioritize order list so the most
  valuable orders survive the cap if the worklist ever produces more than 10 in a turn.

## 8. Expansion Strategy (`strategy/expansion.py`)

- `BUY_LAND`: model payback period (cost / expected incremental $-per-day from the
  new quadrant at current strategy) and only buy when payback fits comfortably before
  day 30. NW→NE→SW→SE cost order is fixed ($1k/$2k/$4k) — confirm via local sim
  whether purchase order among NE/SW/SE is enforced or free (see open question in
  `KNOWLEDGE.md §14`).
- `HIRE`: cost is Fibonacci per day, so hiring N hands is cheap for small N and
  expensive for large N. Rough rule: hire hand `n` if its cost is covered by the
  incremental output that hand can realistically produce before end-of-day drop
  (hands vanish overnight, so per-hire ROI must clear same-day, not amortized).

## 9. Testing Plan

1. **Unit tests** on `state.py` price/yield helpers against the tables in
   `KNOWLEDGE.md` (known input inventory → known price, known watering pattern →
   known yield_units).
2. **Scripted scenario tests**: hand-built fixture `obs` dicts for edge cases —
   two units both trying to plant the last seed, shed at capacity, animal on the
   unfed-day boundary, price at the $1 floor.
3. **Local episode runs** against `"pass"` and `"random"` first (should win trivially
   — if not, something's broken), then against `"starter"` to gauge a real baseline.
4. **Self-play regression**: keep prior agent versions around and run new-vs-old each
   iteration to catch regressions numerically (`env.steps[-1]` reward comparison),
   not just "did it crash."
5. **Replay inspection**: dump `replay.json` on any run with an unexpected score and
   spot-check a few turns manually against the action log to catch silent no-ops.

## 10. Build Order (suggested milestones)

1. `state.py` parsing + `Tile`/`Farm`/`Market` wrappers, unit-tested standalone.
2. Wheat-only loop (extend the `AGENTS.md` example): plant/water/harvest/sell, no
   hands, no land purchases. Get this beating `"random"` reliably.
3. Add carrot + basic tile-priority worklist for >1 concurrent crop.
4. Add shed/inventory routing (`PICKUP`/`DROP`) once produce volume exceeds
   what fits conveniently in a unit's own turn-by-turn harvest→sell cycle.
5. Add `BUY_LAND` + hand hiring once cash flow from step 2–4 supports it.
6. Add ongoing crops (tomato/strawberry) and fertilizer usage.
7. Add animals (goose → cow/sheep), CARE/COLLECT_FERTILIZER logic, wheat-feed
   demand forecasting.
8. Tune phase thresholds and market batching against `"starter"` via repeated local
   runs; log aggregate reward across many seeds (`env.configuration["seed"]`) to avoid
   overfitting to one random weed-spawn draw.
9. Package as `tar.gz` (`main.py` + modules), submit, monitor via
   `kaggle competitions submissions` / `episodes` / `replay` per `AGENTS.md`.

## 11. Risks / Watch-Outs

- **Silent no-ops everywhere** — the game does not raise on invalid actions, so bugs
  manifest as "nothing happened" rather than crashes. Log/assert liberally in local
  testing (not in the submitted agent — keep the submission clean and fast).
- **Simultaneous overplant guard** (`KNOWLEDGE.md §5`/§8): coordinate farmer+hands so
  two units never target the same scarce seed in one turn.
- **Shed overflow discards silently** — a harvest-heavy turn with a near-full shed can
  lose value with no error; the priority worklist needs a shed-capacity check baked in,
  not bolted on later.
- **End-of-day hand loss** — don't strand a hired hand's inventory far from the shed
  near end-of-day; route hands shed-ward proactively as `hour` approaches
  `turnsPerDay - 1`.
- **Price-formula edge cases at the $1 floor** — inventory doesn't move at the floor,
  so `projected_sell_value` needs to special-case this rather than extrapolating the
  curve past it.