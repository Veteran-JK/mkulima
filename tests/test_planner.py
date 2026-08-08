
from kaggle_environments import make

from agent.planner import Planner
from agent.world import GameState


def test_planner_creation():

    env = make("kaggriculture", debug=True)

    obs = env.reset()[0].observation

    state = GameState(obs)

    planner = Planner(state)

    assert planner is not None
    