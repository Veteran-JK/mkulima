import importlib

try:
    make = importlib.import_module("kaggle_environments").make
except ImportError as exc:
    raise RuntimeError(
        "kaggle_environments is required to run this test. "
        "Install it with: pip install kaggle-environments"
    ) from exc

from main import agent

env = make("kaggriculture", debug=True)

env.run([
    agent,
    "random",
])

print("Finished.")