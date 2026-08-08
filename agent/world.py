"""
agent/world.py

Builds a strongly typed GameState from the raw Kaggle observation.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.constants import TOTAL_TURNS, TURNS_PER_DAY
from agent.models.farm import Farm
from agent.models.market import Market


@dataclass(slots=True)
class GameState:
    """
    Represents the complete observable game state for one turn.

    This class contains no decision-making logic.
    It simply exposes the raw observation through strongly typed models.
    """

    player: int

    day: int

    hour: int

    me: Farm

    opponent: Farm

    market: Market

    town: dict

    shed: dict

    seeds: dict

    inventories: list

    configuration: dict

    @classmethod
    def from_observation(
        cls,
        observation,
        configuration,
    ) -> "GameState":
        """
        Construct a GameState from the raw Kaggle observation.
        """

        market = Market.from_dict(
            observation["market"]
        )

        farms = [
            Farm.from_dict(farm)
            for farm in observation["farms"]
        ]

        player = observation["player"]

        return cls(
            player=player,
            day=observation["day"],
            hour=observation["hour"],
            me=farms[player],
            opponent=farms[1 - player],
            market=market,
            town=observation["town"],
            shed=dict(observation["private"]["shed"]),
            seeds=dict(observation["private"]["seeds"]),
            inventories=list(
                observation["private"]["inventories"]
            ),
            configuration=configuration,
        )

    @property
    def current_turn(self) -> int:
        """
        Absolute turn number within the season.
        """
        return self.day * TURNS_PER_DAY + self.hour
    @property
    def turns_remaining(self) -> int:
        """
        Number of turns remaining.
        """
        return TOTAL_TURNS - self.current_turn

    @property
    def is_first_player(self) -> bool:
        """
        True if this agent is player zero.
        """
        return self.player == 0

    def farm(self, player: int) -> Farm:
        """
        Return the farm belonging to a player.
        """
        if player == self.player:
            return self.me

        return self.opponent