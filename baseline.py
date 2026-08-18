import importlib


try:
    make = importlib.import_module("kaggle_environments").make
except ImportError as exc:
    raise RuntimeError(
        "kaggle_environments is required to run this test. "
        "Install it with: pip install kaggle-environments"
    ) from exc


from main import agent


def summarize_player(player_index, state):
    observation = state[player_index]["observation"]

    player = observation["player"]
    farms = observation["farms"]
    market = observation["market"]
    town = observation["town"]

    print(f"\nPLAYER {player_index}")
    print("-" * 40)

    print(f"Reward: {state[player_index].get('reward')}")
    print(f"Status: {state[player_index].get('status')}")
    print(f"Day: {observation.get('day')}")
    print(f"Hour: {observation.get('hour')}")
    print(f"Step: {observation.get('step')}")

    print("\nPlayer:")
    print(f"  {player}")

    print("\nFarms:")
    print(f"  Number of farms: {len(farms)}")

    for i, farm in enumerate(farms):
        print(f"  Farm {i}:")
        print(f"    Money: {farm.get('money')}")
        print(f"    Farmer: {farm.get('farmer')}")
        print(f"    Hands: {farm.get('hands')}")
        print(f"    Unlocked quadrants: {farm.get('unlocked_quadrants')}")

    print("\nMarket:")
    print(f"  Prices: {market.get('prices')}")

    print("\nTown:")
    print(f"  Shops: {town.get('unlocked_shops')}")


def main():
    env = make("kaggriculture", debug=True)

    results = env.run([
        agent,
        "random",
    ])

    state = env.state

    print("=" * 60)
    print("MKULIMA BASELINE")
    print("=" * 60)

    print("\nRESULTS")

    for i, result in enumerate(results):
        print(f"Player {i}: {result}")

    for i in range(len(state)):
        summarize_player(i, state)

    print("\n" + "=" * 60)
    print("BASELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()