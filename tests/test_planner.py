"""
Tests for the Planner.

Current planner scope:

    BuySeedTask
        -> BUY_SEED market action

    PlantTask at farmer's current position
        -> PLANT action

    WaitTask
        -> PASS action
"""

from agent.actions import Actions
from agent.models.position import Position
from agent.planner import Planner
from agent.tasks import BuySeedTask, PlantTask
from agent.world import GameState
from agent.models.tile import Tile
from agent.constants import Crop
from agent.strategy.scheduler import Scheduler
from agent.actions import Actions
from agent.models.position import Position
from agent.planner import Planner
from agent.tasks import BuySeedTask, PlantTask, Task




class DummyScheduler(Scheduler):

    def __init__(self, task: Task):
        self.task = task

    def choose_task(
        self,
        state: GameState,
    ) -> Task:
        return self.task


def make_planner(task, state):
    """
    Create a Planner with a controlled task.
    """

    planner = Planner(state)
    planner.scheduler = DummyScheduler(task)

    return planner


def make_state():
    """
    Build a minimal state containing a small walkable farm.
    """

    class Farmer:
        position = Position(0, 0)

    class Farm:
        farmer = Farmer()
        width = 5

        def tile_at(self, position):
            return Tile(
                position=position,
                unlocked=True,
            )

    class State:
        me = Farm()

    return State()

def test_planner_executes_buy_seed_task():
    """
    BuySeedTask should become a BUY_SEED market action.
    """

    state = make_state()

    task = BuySeedTask(
        crop=Crop.WHEAT,
        quantity=1,
    )

    planner = make_planner(task, state)

    result = planner.plan()

    assert result["market"] == [
        ["BUY_SEED", "WHEAT", 1]
    ]

    assert result["hands"] == []


def test_planner_executes_plant_task_at_target():
    """
    PlantTask should become a PLANT action when the farmer
    is already standing on the target tile.
    """

    state = make_state()

    task = PlantTask(
        target=Position(0, 0),
        crop=Crop.WHEAT,
    )

    planner = make_planner(task, state)

    result = planner.plan()

    assert result["farmer"] == [
        "PLANT",
        "WHEAT",
    ]


def test_planner_moves_toward_plant_target():
    """
    A PlantTask whose target is elsewhere should produce
    the first movement direction toward that target.
    """

    state = make_state()

    task = PlantTask(
        target=Position(3, 0),
        crop=Crop.WHEAT,
    )

    planner = make_planner(task, state)

    result = planner.plan()

    assert result["farmer"] == [
        "EAST",
    ]

    