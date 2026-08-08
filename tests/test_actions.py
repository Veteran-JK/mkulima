"""
Actions tests.
"""

from agent.actions import Actions


def test_actions_creation():

    actions = Actions()

    assert actions is not None


def test_actions_dict():

    actions = Actions()

    result = actions.to_dict()

    assert isinstance(result, dict)