"""E0 - environment validation. Run: python3 -m unittest discover -s tests -v"""
import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pgg.agents import Adaptive, Cooperative, Reciprocal, Selfish, play_repeated
from pgg.game import Game, gini
from pgg.llm import parse_amount
from pgg.prompts import VARIANTS, comprehension_items, implied_payoff

MPCRS = [0.2, 0.3, 0.4, 0.5, 0.75, 1.25]


def games():
    return [Game(n=4, endowment=20, r=m * 4) for m in MPCRS] + [Game(n=10, endowment=20, r=2)]


class TestPayoffs(unittest.TestCase):
    def test_reference_profiles(self):
        g = Game(4, 20, 1.6)
        self.assertEqual(g.payoffs([0, 0, 0, 0]), [20, 20, 20, 20])
        self.assertTrue(all(abs(p - 32) < 1e-9 for p in g.payoffs([20] * 4)))
        # free rider among three full contributors
        p = g.payoffs([0, 20, 20, 20])
        self.assertAlmostEqual(p[0], 20 + 1.6 * 60 / 4)
        self.assertAlmostEqual(p[1], 1.6 * 60 / 4)

    def test_welfare_identity(self):
        rng = random.Random(1)
        for g in games():
            for _ in range(200):
                c = [rng.randint(0, g.endowment) for _ in range(g.n)]
                self.assertAlmostEqual(g.welfare(c), g.n * g.endowment + (g.r - 1) * sum(c))

    def test_regimes_and_dominance(self):
        expected = {0.2: ("control_inefficient", 0, 0), 0.3: ("dilemma", 0, 20), 0.4: ("dilemma", 0, 20),
                    0.5: ("dilemma", 0, 20), 0.75: ("dilemma", 0, 20), 1.25: ("control_dominant", 20, 20)}
        for m, (regime, dom, opt) in expected.items():
            g = Game(4, 20, m * 4)
            self.assertEqual(g.regime, regime)
            self.assertEqual(g.dominant_action(), dom)
            self.assertEqual(g.welfare_optimum_action(), opt)

    def test_dominant_action_by_enumeration(self):
        """For every profile of the others on a grid, the dominant action is a best response."""
        for m in MPCRS:
            g = Game(4, 20, m * 4)
            for others in itertools.product([0, 7, 20], repeat=3):
                best = max(range(21), key=lambda c: g.payoffs([c, *others])[0])
                self.assertEqual(best, g.dominant_action())

    def test_one_shot_regret_is_rescaled_contribution(self):
        g = Game(4, 20, 1.6)
        for c in range(21):
            others = [5, 9, 13]
            regret = max(g.payoffs([a, *others])[0] for a in range(21)) - g.payoffs([c, *others])[0]
            self.assertAlmostEqual(regret, c * (1 - g.mpcr))

    def test_validation(self):
        g = Game(4, 20, 1.6)
        for bad in (-1, 21, 3.5, "5", None, True):
            self.assertFalse(g.validate(bad))
        with self.assertRaises(ValueError):
            g.payoffs([0, 0, 0])
        with self.assertRaises(ValueError):
            g.payoffs([0, 0, 0, 25])

    def test_efficiency_and_gini(self):
        g = Game(4, 20, 1.6)
        self.assertAlmostEqual(g.efficiency([0] * 4), 0)
        self.assertAlmostEqual(g.efficiency([20] * 4), 1)
        self.assertAlmostEqual(g.efficiency([10] * 4), 0.5)
        self.assertAlmostEqual(gini([5, 5, 5, 5]), 0)
        self.assertAlmostEqual(gini([0, 0, 0, 10]), 0.75)


class TestPrompts(unittest.TestCase):
    def test_payoff_equivalence_across_variants(self):
        """Every variant's text implies the engine's payoff for the mapped contributions."""
        rng = random.Random(7)
        for g in [Game(4, 20, m * 4) for m in MPCRS]:
            for name, build in VARIANTS.items():
                _, conv = build(g)
                for _ in range(100):
                    answers = [rng.randint(0, g.endowment) for _ in range(g.n)]
                    contributions = [conv(a) for a in answers]
                    self.assertAlmostEqual(
                        implied_payoff(name, g, answers[0], answers[1:]),
                        g.payoffs(contributions)[0],
                        msg=f"{name} m={g.mpcr}",
                    )

    def test_parameters_appear_in_text(self):
        for g in [Game(4, 20, m * 4) for m in MPCRS]:
            for name, build in VARIANTS.items():
                text, _ = build(g)
                shown = f"{g.mpcr:.4f}".rstrip("0").rstrip(".") if name == "P2" else f"{g.r:.4f}".rstrip("0").rstrip(".")
                self.assertIn(shown, text, msg=name)
                self.assertIn(str(g.endowment), text)
                self.assertIn('"amount"', text)

    def test_neutral_variants_avoid_loaded_words(self):
        g = Game(4, 20, 1.6)
        for name in ("P0", "P1", "P2", "P3", "P4", "F1"):
            text = VARIANTS[name](g)[0].lower()
            for word in ("public", "cooperat", "contribut", "game", "invest", "team", "group", "fair"):
                self.assertNotIn(word, text, msg=f"{name}: {word}")

    def test_comprehension_answers(self):
        g = Game(4, 20, 1.6)
        items = dict((k, a) for k, _, a in comprehension_items(g))
        self.assertAlmostEqual(items["own_full_others_zero"], g.payoffs([20, 0, 0, 0])[0])
        self.assertAlmostEqual(items["own_zero_others_full"], g.payoffs([0, 20, 20, 20])[0])


class TestParsing(unittest.TestCase):
    def test_parse_amount(self):
        self.assertEqual(parse_amount('{"amount": 12}', 20), 12)
        self.assertEqual(parse_amount('```json\n{"amount": 0}\n```', 20), 0)
        self.assertEqual(parse_amount('I choose.\n{"amount": 20.0}', 20), 20)
        for bad in ('{"amount": 21}', '{"amount": -1}', '{"amount": "ten"}', "12", "", '{"amount": 3.5}', '{"other": 3}'):
            self.assertIsNone(parse_amount(bad, 20), msg=bad)


class TestRuleAgents(unittest.TestCase):
    def test_trajectories(self):
        g = Game(4, 20, 1.6)
        log = play_repeated(g, [Selfish()] * 4, 5)
        self.assertTrue(all(r["contributions"] == [0] * 4 for r in log))
        log = play_repeated(g, [Cooperative()] * 4, 5)
        self.assertTrue(all(r["contributions"] == [20] * 4 for r in log))
        log = play_repeated(g, [Reciprocal(), Selfish(), Selfish(), Selfish()], 3)
        self.assertEqual([r["contributions"][0] for r in log], [10, 0, 0])

    def test_seed_reproducibility(self):
        g = Game(4, 20, 1.6)
        runs = []
        for _ in range(2):
            rng = random.Random(42)
            agents = [Adaptive(), Adaptive(), Reciprocal(), Selfish()]
            runs.append(play_repeated(g, agents, 30, rng))
        self.assertEqual(runs[0], runs[1])


if __name__ == "__main__":
    unittest.main()
