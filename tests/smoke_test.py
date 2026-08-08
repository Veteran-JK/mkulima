"""
Smoke test.

Run manually.

python tests/smoke_test.py
"""

from agent.actions import Actions
from agent.strategy.scheduler import Scheduler

print("Creating Scheduler...")
scheduler = Scheduler()
print("✓ Scheduler created")

print("Creating Actions...")
actions = Actions()
print("✓ Actions created")

print("Done.")