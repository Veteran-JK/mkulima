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


results = env.run([
    agent,
    "random",
])


print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

for i, result in enumerate(results):
    print(f"Player {i}: {result}")

print("\n" + "=" * 60)
print("ENVIRONMENT STATE")
print("=" * 60)

print(env.state)