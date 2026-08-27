import importlib
from collections import Counter


try:
    make = importlib.import_module("kaggle_environments").make
except ImportError as exc:
    raise RuntimeError(
        "kaggle_environments is required to run this test. "
        "Install it with: pip install kaggle-environments"
    ) from exc


from main import agent


actions = []


def tracked_agent(observation, configuration):
    """Run Mkulima while recording every returned action."""

    action = agent(observation, configuration)

    actions.append(action)

    return action


def action_name(action):
    """Extract a readable action name from the returned action."""

    if isinstance(action, dict):
        return action.get("action", str(action))

    return str(action)


def main():
    env = make("kaggriculture", debug=True)

    results = env.run([
        tracked_agent,
        "random",
    ])

    print("=" * 60)
    print("MKULIMA BASELINE v0.1")
    print("=" * 60)

    print("\nRESULTS")

    for i, result in enumerate(results):
        print(f"Player {i}: {result}")

    print("\nACTION COUNTS")
    print("-" * 40)

    counts = Counter(
        action_name(action)
        for action in actions
    )

    for action, count in counts.most_common():
        print(f"{action:<20} {count}")

    print("\nTOTAL ACTIONS")
    print("-" * 40)
    print(len(actions))

    print("\nFINAL ENVIRONMENT STATUS")
    print("-" * 40)

    for i, player in enumerate(env.state):
        print(
            f"Player {i}: "
            f"status={player.get('status')}, "
            f"reward={player.get('reward')}"
        )

    print("\n" + "=" * 60)
    print("BASELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()