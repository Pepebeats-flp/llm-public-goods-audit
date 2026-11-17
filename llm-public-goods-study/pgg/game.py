"""Game engine. All payoffs are computed here; LLMs never compute official results."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    n: int = 4          # players
    endowment: int = 20  # points per player
    r: float = 1.6      # multiplier of the shared account

    @property
    def mpcr(self) -> float:
        return self.r / self.n

    @property
    def regime(self) -> str:
        if self.r < 1:
            return "control_inefficient"   # zero is dominant and welfare-maximising
        if self.r > self.n:
            return "control_dominant"      # full contribution is dominant and welfare-maximising
        if 1 < self.r < self.n:
            return "dilemma"
        return "boundary"

    def validate(self, c) -> bool:
        return isinstance(c, int) and not isinstance(c, bool) and 0 <= c <= self.endowment

    def payoffs(self, contributions):
        if len(contributions) != self.n or not all(self.validate(c) for c in contributions):
            raise ValueError(f"invalid contribution profile: {contributions}")
        share = self.r * sum(contributions) / self.n
        return [self.endowment - c + share for c in contributions]

    def welfare(self, contributions) -> float:
        return sum(self.payoffs(contributions))

    def dominant_action(self):
        """One-shot dominant contribution under monetary payoffs (None on the boundary)."""
        if self.mpcr < 1:
            return 0
        if self.mpcr > 1:
            return self.endowment
        return None

    def welfare_optimum_action(self):
        if self.r > 1:
            return self.endowment
        if self.r < 1:
            return 0
        return None

    def efficiency(self, contributions) -> float:
        """(W - W_dominant) / (W_opt - W_dominant); only defined inside the dilemma."""
        if self.regime != "dilemma":
            raise ValueError("efficiency is only defined inside the dilemma range")
        w0 = self.welfare([0] * self.n)
        w1 = self.welfare([self.endowment] * self.n)
        return (self.welfare(contributions) - w0) / (w1 - w0)


def gini(values) -> float:
    xs = sorted(values)
    n, tot = len(xs), sum(xs)
    if n == 0 or tot == 0:
        return 0.0
    return sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(xs)) / (n * tot)
