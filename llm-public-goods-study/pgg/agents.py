"""Rule-based reference agents for the repeated game."""
import random


class Selfish:
    name = "selfish"

    def act(self, game, history, rng=None):
        return 0


class Cooperative:
    name = "cooperative"

    def act(self, game, history, rng=None):
        return game.endowment


class Reciprocal:
    """Matches the rounded mean contribution of the others in the previous round."""
    name = "reciprocal"

    def act(self, game, history, rng=None):
        if not history:
            return game.endowment // 2
        return int(round(history[-1]["others_mean"]))


class Adaptive:
    """Non-linguistic learner: EMA of own payoff per action on a coarse grid, epsilon-greedy."""
    name = "adaptive"

    def __init__(self, alpha=0.3, epsilon=0.1, grid=5):
        self.alpha, self.epsilon, self.grid = alpha, epsilon, grid
        self.q = {}

    def act(self, game, history, rng=None):
        rng = rng or random
        actions = sorted({round(i * game.endowment / (self.grid - 1)) for i in range(self.grid)})
        if history:
            last = history[-1]
            a = min(actions, key=lambda x: abs(x - last["own"]))
            old = self.q.get(a, last["payoff"])
            self.q[a] = (1 - self.alpha) * old + self.alpha * last["payoff"]
        untried = [a for a in actions if a not in self.q]
        if untried:
            return rng.choice(untried)
        if rng.random() < self.epsilon:
            return rng.choice(actions)
        return max(actions, key=lambda a: self.q[a])


def play_repeated(game, agents, rounds, rng=None):
    """Simultaneous-move repeated game. Each agent sees own payoff and others' mean."""
    histories = [[] for _ in agents]
    log = []
    for t in range(rounds):
        cs = [ag.act(game, h, rng) for ag, h in zip(agents, histories)]
        ps = game.payoffs(cs)
        for i, h in enumerate(histories):
            others = [c for j, c in enumerate(cs) if j != i]
            h.append({"round": t + 1, "own": cs[i], "payoff": ps[i], "others_mean": sum(others) / len(others)})
        log.append({"round": t + 1, "contributions": cs, "payoffs": ps})
    return log
