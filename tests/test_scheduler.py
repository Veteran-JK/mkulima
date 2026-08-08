"""
Scheduler tests.
"""

from agent.strategy.scheduler import Scheduler


def test_scheduler_creation():

    scheduler = Scheduler()

    assert scheduler is not None
    assert len(scheduler.strategies) > 0