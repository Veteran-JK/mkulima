"""
agent/models/market.py

Represents the public market state.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Market:
    """
    Represents the observable market.

    Attributes
    ----------
    inventory : dict[str, int]
        Current quantity of every product in the market.

    prices : dict[str, float]
        Current market price of every product.
    """

    inventory: dict[str, int] = field(default_factory=dict)

    prices: dict[str, float] = field(default_factory=dict)

    @property
    def products(self) -> tuple[str, ...]:
        """
        Return all products currently tracked by the market.
        """
        return tuple(self.inventory.keys())

    def inventory_of(self, product: str) -> int:
        """
        Return the current inventory of a product.

        Unknown products return zero.
        """
        return self.inventory.get(product, 0)

    def price_of(self, product: str) -> float:
        """
        Return the current market price of a product.

        Unknown products return 0.
        """
        return self.prices.get(product, 0.0)

    def contains(self, product: str) -> bool:
        """
        Return True if the market tracks the product.
        """
        return product in self.inventory

    def __contains__(self, product: str) -> bool:
        """
        Allow:

            if "WHEAT" in market:
                ...
        """
        return product in self.inventory

    def __getitem__(self, product: str) -> float:
        """
        Allow:

            market["WHEAT"]

        Returns the current market price.
        """
        return self.price_of(product)

    def __repr__(self) -> str:
        return (
            f"Market("
            f"products={len(self.inventory)}, "
            f"prices={len(self.prices)})"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Market":
        """
        Create a Market from a raw observation dictionary.
        """
        return cls(
            inventory=dict(data["inventory"]),
            prices=dict(data["prices"]),
        )