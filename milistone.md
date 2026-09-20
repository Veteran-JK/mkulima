Mkulima roadmap
✅ Milestone 1 — Project architecture

Status: COMPLETE

Established the basic separation of responsibilities:

GameState
    ↓
Scheduler
    ↓
Strategy
    ↓
Task
    ↓
Planner
    ↓
Action
    ↓
Kaggriculture

Key components established:

GameState
Models for farm, tiles, plants, animals, market, positions, workers
Constants/enums
Tasks
Strategies
Scheduler
Planner
Actions
Pathfinding
Kaggle entry point

The important architectural principle is:

Strategy decides WHAT. Planner decides HOW.

✅ Milestone 2 — World/state representation

Status: COMPLETE

GameState.from_observation() can transform the Kaggriculture observation into our internal representation.

We can access things such as:

state.day
state.hour
state.me
state.opponent
state.market
state.seeds
state.shed
state.inventories
state.configuration

We also added:

state.current_turn
state.turns_remaining
state.is_first_player
state.farm(...)
✅ Milestone 3 — Action abstraction

Status: COMPLETE

Established the action layer rather than constructing raw Kaggriculture dictionaries throughout the agent.

We have abstractions such as:

buy_seed(...)
move(...)
plant(...)
wait(...)

and:

Actions()

which produces the final environment-compatible dictionary.

Tests cover the action construction.

✅ Milestone 4 — Opening strategy

Status: COMPLETE

The opening strategy detects the initial condition:

No wheat seed
       ↓
Buy 1 wheat seed

and stops buying once the seed exists.

Verified against the real Kaggriculture environment, not merely mocks.

✅ Milestone 5 — Basic farming strategy

Status: COMPLETE

FarmingStrategy currently:

checks whether wheat seeds exist;
searches for an unlocked empty tile;
creates a PlantTask;
targets the first suitable tile.

Currently:

WHEAT seed
   ↓
find empty unlocked tile
   ↓
PlantTask(WHEAT, target)

This is intentionally simplistic. We haven't optimized crop selection yet.

✅ Milestone 6 — Pathfinding

Status: COMPLETE

Implemented reusable navigation utilities:

Manhattan distance
adjacency
neighbor generation
direction calculation
walkability
BFS
path reconstruction
next_step()

This gives the Planner the ability to translate:

"Plant at (0,0)"

into:

NORTH
NORTH
WEST
...

one movement action per turn.

✅ Milestone 7 — Planner

Status: COMPLETE

The Planner can currently translate:

BuySeedTask
    → BUY_SEED

PlantTask at current position
    → PLANT

PlantTask elsewhere
    → MOVE

WaitTask
    → PASS

We also fixed the Pylance typing issue around the test scheduler.

Planner tests currently verify:

buying
planting
movement
continued movement
one movement step per turn
✅ Milestone 8 — Scheduler

Status: COMPLETE

Established the priority chain:

Emergency
   ↓
Opening
   ↓
Farming
   ↓
Livestock
   ↓
Market
   ↓
Economy
   ↓
Expansion
   ↓
Wait

The scheduler selects the first strategy that proposes a task.

The other strategies exist structurally, but most are not yet operational.

✅ Milestone 9 — Integration with real Kaggriculture

Status: COMPLETE

This is important.

We moved beyond isolated unit tests and verified the actual environment.

We successfully tested:

Real environment
      ↓
observation
      ↓
GameState
      ↓
Planner
      ↓
BUY_SEED
      ↓
real environment
      ↓
new observation
      ↓
GameState
      ↓
FarmingStrategy
      ↓
PlantTask
      ↓
movement
      ↓
planting

The integration tests currently pass.

✅ Milestone 10 — Full-agent execution

Status: COMPLETE

main.py is now a genuine Kaggriculture entry point:

def agent(observation, configuration):
    state = GameState.from_observation(...)
    planner = Planner(state)
    return planner.plan()

And:

python run.py

successfully runs:

Mkulima
   vs
random

through the actual environment.

We have therefore crossed an important boundary:

Mkulima is no longer just a collection of tested components. It is an executable game-playing agent.

✅ Milestone 11 — Full-season baseline execution

Status: ACHIEVED / BASELINE READY

Your run.py now executes the environment and exposes the complete env.state.

We have observed the agent reaching deep into the season, e.g.:

day: 28
hour: 21
step: 694
status: ACTIVE

This gives us access to actual game behavior rather than hypothetical behavior.

We have not yet completed the formal baseline analysis, however.

That distinction matters.

Remaining milestones

Now the project becomes substantially more interesting.

🟡 Milestone 12 — Baseline instrumentation

Next

Build a compact diagnostic layer that records:

turn
action
position
money
seeds
plants
watered crops
harvests
sales
PASS count
movement count

and produces something like:

Mkulima v0.1
────────────────────
Final money:       XXXX
Final reward:      XXXX

BUY:                 X
MOVE:                X
PLANT:               X
WATER:               0
HARVEST:             0
SELL:                0
PASS:              XXX

This becomes our quantitative baseline.

🟡 Milestone 13 — Crop lifecycle

Next major development

Implement:

Seed
 ↓
Plant
 ↓
Water
 ↓
Growth
 ↓
Harvest
 ↓
Product

Initially we can focus on wheat.

This is the first point where Mkulima starts generating an economic return from farming rather than merely performing actions.

🟡 Milestone 14 — Crop-state awareness

The strategy must stop thinking simply:

"Do I have seeds?"

and start reasoning:

What crops exist?
What stage are they in?
Which need water?
Which can be harvested?
Which have fertilizer effects?

This will require the world model to expose the relevant plant state cleanly.

🟡 Milestone 15 — Farming task scheduling

We need to move from:

PlantTask

to a lifecycle-aware task system:

PlantTask
WaterTask
HarvestTask
FertilizeTask

and eventually prioritize them.

For example:

Harvest ready crop
      >
Water crop that needs water
      >
Plant available seed
      >
Other work
🟡 Milestone 16 — Locality-aware farming

This addresses the concern you raised earlier.

Currently the strategy can choose:

Farmer: (4,4)
Target: (0,0)

and spend several turns walking there.

We need the strategy to understand:

A turn has opportunity cost.

Instead of blindly selecting the first tile, it should consider:

distance
expected yield
crop state
available actions
remaining turns
worker availability

This is where Mkulima starts becoming an actual planning agent rather than a rule executor.

🟡 Milestone 17 — Harvest → inventory → selling

Complete the economic loop:

Farm
 ↓
Harvest
 ↓
Inventory
 ↓
Market
 ↓
Sell
 ↓
Money

Then verify it against the real environment.

🟡 Milestone 18 — Market strategy

Introduce actual economic decisions:

What should we buy?
What should we sell?
When?
How much?

Initially this can be rule-based.

Later we can introduce:

price history
expected revenue
opportunity cost
market trends
forecasting
🟡 Milestone 19 — Multiple crops

Move beyond hard-coded wheat:

WHEAT
CARROT
TOMATO
STRAWBERRY
MELON

Develop crop selection based on:

seed cost
growth time
yield
selling price
expected profit
water requirements
fertilizer effects
remaining season
🟡 Milestone 20 — Fertilizer optimization

Implement:

Fertilize
    ↓
3-day yield effect

and determine when fertilizer has positive expected value.

This should eventually become an optimization problem rather than a fixed rule.

🟡 Milestone 21 — Worker management

Introduce farm hands properly:

Farmer
FarmHand 1
FarmHand 2
...

Then distribute tasks according to:

distance
availability
task priority
action economy

Eventually:

Worker → Task assignment

becomes its own scheduling problem.

🟡 Milestone 22 — Livestock

Implement the animal lifecycle:

Buy animal
 ↓
Feed
 ↓
Care
 ↓
Produce
 ↓
Collect
 ↓
Sell

for:

GOOSE
COW
SHEEP
🟡 Milestone 23 — Land and expansion

Implement:

BUY_LAND

and determine whether expansion is economically justified.

The agent should not expand simply because land is available.

It should ask:

Expected additional profit
        >
Cost of expansion?
🟡 Milestone 24 — Emergency/risk management

Make EmergencyStrategy actually useful.

Examples:

animal about to die
crop requiring immediate action
critical resource shortage
insufficient cash
season ending

Emergency tasks should override normal economic optimization.

🟡 Milestone 25 — End-of-season liquidation

The agent needs explicit awareness of:

turns_remaining

Near the end:

No long-duration investments
No unnecessary planting
Harvest everything possible
Sell inventory
Preserve cash

The objective is ultimately:

maximize final bank balance.

🟡 Milestone 26 — Full-season optimization

At this point we stop thinking in isolated actions and start evaluating the 720-turn horizon.

The agent should reason about:

Current state
      ↓
Possible actions
      ↓
Future consequences
      ↓
Expected final wealth

This is where heuristics, dynamic priorities and eventually forecasting become useful.

🟡 Milestone 27 — Baseline Kaggle submission

Once we have a minimally competent full-season agent:

Mkulima v0.x
      ↓
Kaggle submission
      ↓
score
      ↓
rank

This should happen before the agent is "finished."

The submission becomes an external benchmark.

🟡 Milestone 28 — Kaggle experimental loop

Then we enter the real optimization cycle:

                ┌──────────────┐
                │ Kaggle score │
                └──────┬───────┘
                       ↓
                 Find weakness
                       ↓
                Form hypothesis
                       ↓
                  Implement
                       ↓
                    Tests
                       ↓
               Local simulation
                       ↓
                Kaggle submission
                       ↓
                    Compare
                       │
                       └──────────→

For every version we should record:

Version
Change
Local performance
Kaggle score
Observed weakness
Decision
🟢 Milestone 29 — Advanced optimization

Only after the rule-based agent is strong should we consider:

dynamic priorities
market forecasting
statistical price models
Monte Carlo simulation
reinforcement learning
search/planning
learned crop profitability
opponent modeling

Your existing configuration already hints at this future:

USE_HEURISTICS = True
USE_MARKET_FORECAST = False
USE_DYNAMIC_PRIORITIES = False

Those should be activated progressively, not prematurely.

🟢 Milestone 30 — Final competitive agent

The final architecture should roughly become:

                 OBSERVATION
                      │
                      ▼
                ┌───────────┐
                │ GameState │
                └─────┬─────┘
                      │
                      ▼
              ┌───────────────┐
              │ World Model   │
              └───────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Farming     Livestock    Market
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Scheduler
                      │
                      ▼
                 Task Queue
                      │
                      ▼
                   Planner
                      │
                      ▼
                   Actions
                      │
                      ▼
                 Kaggriculture
                      │
                      └──────► telemetry
Where we are right now

The most accurate status is:

Milestone	Status
Architecture	✅
World model	✅
Actions	✅
Opening	✅
Basic farming	✅
Pathfinding	✅
Planner	✅
Scheduler	✅
Unit tests	✅
Real-environment integration	✅
Full-agent execution	✅
Full-season execution	✅
Baseline instrumentation	← NEXT
Crop lifecycle	⬜
Watering	⬜
Harvesting	⬜
Farming scheduling	⬜
Locality/opportunity-cost planning	⬜
Selling/economy loop	⬜
Market strategy	⬜
Multi-crop optimization	⬜
Fertilizer optimization	⬜
Worker management	⬜
Livestock	⬜
Expansion	⬜
Emergency/risk management	⬜
End-season optimization	⬜
Full-season optimization	⬜
First Kaggle baseline submission	⬜
Kaggle iterative optimization	⬜
Advanced modeling/forecasting	⬜
Competitive final agent