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


class TestRepeatedGame(unittest.TestCase):
    """Study 2, part B: prompts and runner of the repeated game."""

    def setUp(self):
        from pgg.prompts import REPEATED_VARIANTS, repeated_prompt
        from pgg.run_repeated import play_game
        self.variants, self.prompt, self.play = REPEATED_VARIANTS, repeated_prompt, play_game
        self.g = Game(4, 20, 1.6)

    def test_prompt_states_rule_and_history(self):
        hist = [{"round": 1, "own": 10, "others_mean": 20 / 3, "payoff": self.g.payoffs([10, 20, 0, 0])[0]}]
        for v in self.variants:
            text, conv = self.prompt(v, self.g, 10, 2, hist)
            for token in ("1.6", "20", "10 rounds", "round 2 of 10", '"amount"', "6.7", "22"):
                self.assertIn(token, text, msg=f"{v}: {token}")
            self.assertEqual(conv(7), 7)
            first, _ = self.prompt(v, self.g, 10, 1, [])
            self.assertIn("No rounds have been played yet.", first)

    def test_recorded_payoffs_match_engine(self):
        """Every recorded payoff and others' mean equals the engine's value for that round's profile."""
        rng = random.Random(3)
        plan = [[rng.randint(0, 20) for _ in range(4)] for _ in range(6)]
        calls = {"n": 0}

        def decide(seat, prompt, parse):
            t = calls["n"] // 4
            calls["n"] += 1
            return plan[t][seat], [{"valid": True, "attempt": 1, "contribution": plan[t][seat]}]

        status, rows = self.play(self.g, 6, ["llm"] * 4, "P0", decide)
        self.assertEqual(status, "complete")
        self.assertEqual(len(rows), 24)
        for r in rows:
            profile = plan[r["round"] - 1]
            self.assertEqual(r["contribution"], profile[r["seat"]])
            self.assertAlmostEqual(r["payoff"], self.g.payoffs(profile)[r["seat"]])
            self.assertAlmostEqual(r["others_mean"], (sum(profile) - profile[r["seat"]]) / 3)
            self.assertEqual(r["round_total"], sum(profile))

    def test_agents_see_only_their_own_history(self):
        seen = {}

        def decide(seat, prompt, parse):
            seen.setdefault(seat, []).append(prompt)
            return [0, 5, 10, 20][seat], [{"valid": True, "attempt": 1, "contribution": [0, 5, 10, 20][seat]}]

        status, rows = self.play(self.g, 3, ["llm"] * 4, "P0", decide)
        self.assertEqual(status, "complete")
        pay = self.g.payoffs([0, 5, 10, 20])
        for seat, own in enumerate([0, 5, 10, 20]):
            others = (35 - own) / 3
            line = f"Round 1: you placed {own}, the others placed {others:.1f}".rstrip("0").rstrip(".")
            self.assertIn(line, seen[seat][1])
            self.assertIn(f"{pay[seat]:.2f}".rstrip("0").rstrip("."), seen[seat][1])
            self.assertEqual(seen[seat][2].count("Round "), 2)

    def test_neutral_repeated_prompt_avoids_loaded_words(self):
        text = self.prompt("P0", self.g, 10, 1, [])[0].lower()
        for word in ("public", "cooperat", "contribut", "game", "invest", "team", "group", "fair"):
            self.assertNotIn(word, text)

    def test_one_selfish_seat_and_discard_rules(self):
        status, rows = self.play(self.g, 4, ["llm", "llm", "llm", "selfish"], "P0",
                                 lambda seat, prompt, parse: (20, [{"valid": True, "attempt": 1}]))
        self.assertEqual(status, "complete")
        self.assertTrue(all(r["contribution"] == 0 for r in rows if r["agent_type"] == "selfish"))
        self.assertAlmostEqual(next(r["payoff"] for r in rows if r["agent_type"] == "selfish"), 20 + 1.6 * 60 / 4)
        # two invalid outputs discard the group; a transport failure abandons it
        bad = lambda seat, prompt, parse: (None, [{"valid": False, "attempt": 1}, {"valid": False, "attempt": 2}])
        self.assertEqual(self.play(self.g, 4, ["llm"] * 4, "P0", bad)[0], "discarded")
        down = lambda seat, prompt, parse: (None, [{"valid": False, "attempt": 1, "transport_failed": True}])
        self.assertEqual(self.play(self.g, 4, ["llm"] * 4, "P0", down)[0], "transport_failed")


class TestPrisonersDilemma(unittest.TestCase):
    """Study 3: payoffs, prompts and runner of the prisoner's dilemma."""

    MS = [0.4, 0.6, 0.7, 0.8, 0.9, 1.25]

    def setUp(self):
        from pgg import pd
        self.pd = pd

    def test_payoff_order_and_regimes(self):
        for m in self.MS:
            g = self.pd.PD(20, m)
            self.assertAlmostEqual(g.payoff(True, True), g.R)
            self.assertAlmostEqual(g.payoff(False, True), g.T)
            self.assertAlmostEqual(g.payoff(False, False), g.P)
            self.assertAlmostEqual(g.payoff(True, False), g.S)
            for v in (g.R, g.T, g.P, g.S):
                self.assertAlmostEqual(v, round(v))             # integer payoffs in every condition
            if 0.5 < m < 1:
                self.assertEqual(g.regime, "dilemma")
                self.assertTrue(g.T > g.R > g.P > g.S)
                self.assertTrue(2 * g.R > g.T + g.S)            # mutual cooperation beats alternation
            # dominance by enumeration
            for other in (True, False):
                best = max((True, False), key=lambda own: g.payoff(own, other))
                self.assertEqual(best, g.dominant_cooperates())
        self.assertEqual(self.pd.PD(20, 0.4).regime, "control_inefficient")
        self.assertTrue(self.pd.PD(20, 0.4).P > self.pd.PD(20, 0.4).R)       # defecting is also efficient
        self.assertEqual(self.pd.PD(20, 1.25).regime, "control_dominant")

    def test_variant_texts_imply_engine_payoffs(self):
        for m in self.MS:
            g = self.pd.PD(20, m)
            for name in self.pd.VARIANTS:
                for own in (True, False):
                    for other in (True, False):
                        self.assertAlmostEqual(self.pd.implied_payoff(name, g, own, other), g.payoff(own, other), msg=f"{name} m={m}")

    def test_numbers_and_labels_in_text(self):
        """Each table states the four payoffs next to the right pair of labels, under both label assignments."""
        import re
        for m in self.MS:
            g = self.pd.PD(20, m)
            for coop_first in (True, False):
                text, labels = self.pd.VARIANTS["P0"](g, coop_first)
                self.assertEqual(labels, {"A": coop_first, "B": not coop_first})
                both = dict(re.findall(r"If you both choose ([AB]), each of you receives ([\d.]+) points", text))
                for lab, val in both.items():
                    self.assertAlmostEqual(float(val), g.R if labels[lab] else g.P)
                mixed = re.findall(r"If you choose ([AB]) and the other participant chooses ([AB]), you receive ([\d.]+) points "
                                   r"and the other participant receives ([\d.]+) points", text)
                self.assertEqual(len(both), 2)
                self.assertEqual(len(mixed), 2)
                for own, oth, a, b in mixed:
                    self.assertAlmostEqual(float(a), g.payoff(labels[own], labels[oth]))
                    self.assertAlmostEqual(float(b), g.payoff(labels[oth], labels[own]))
                # the outcomes are always listed in the order AA, BB, AB, BA
                self.assertLess(text.index("both choose A"), text.index("both choose B"))

    def test_take_frame_text(self):
        g = self.pd.PD(20, 0.7)
        text, labels = self.pd.VARIANTS["F1"](g, True)
        self.assertIn("starts with 28 points", text)
        self.assertIn("Option B adds 6 points to your points and removes 14 points from the points of the other participant", text)
        self.assertEqual(labels, {"A": True, "B": False})

    def test_neutral_variants_avoid_loaded_words(self):
        g = self.pd.PD(20, 0.7)
        for name in ("P0", "P1", "P2", "P3", "P4", "F1"):
            text = self.pd.VARIANTS[name](g, True)[0].lower()
            for word in ("prison", "dilemma", "cooperat", "defect", "betray", "game", "team", "partner", "trust", "fair"):
                self.assertNotIn(word, text, msg=f"{name}: {word}")
        named = self.pd.VARIANTS["F3"](g, True)[0].lower()
        self.assertIn("prisoner's dilemma", named)

    def test_parse_choice(self):
        ab = {"A": True, "B": False}
        self.assertIs(self.pd.parse_choice('{"choice": "A"}', ab), True)
        self.assertIs(self.pd.parse_choice('```json\n{"choice": "b"}\n```', ab), False)
        cd = {"cooperate": True, "defect": False}
        self.assertIs(self.pd.parse_choice('I think. {"choice": "Defect"}', cd), False)
        for bad in ('{"choice": "C"}', '{"choice": 1}', "A", "", '{"amount": 20}', '{"choice": "cooperate"}'):
            self.assertIsNone(self.pd.parse_choice(bad, ab), msg=bad)

    def test_comprehension_answers(self):
        g = self.pd.PD(20, 0.7)
        for coop_first in (True, False):
            items = {k: a for k, _, a in self.pd.comprehension_items(g, coop_first)}
            self.assertAlmostEqual(items["own_coop_other_defect"], 14)
            self.assertAlmostEqual(items["own_defect_other_coop"], 34)

    def test_repeated_game_through_shared_runner(self):
        """The repeated runner with the prisoner's dilemma prompt: payoffs, history text and label mapping."""
        from pgg.run_repeated import play_game
        g = self.pd.PD(20, 0.7)
        seen = {}
        plan = {0: [True, False, True], 1: [False, False, True]}      # seat -> cooperation by round
        calls = {0: 0, 1: 0}

        def prompt_fn(variant, game, rounds, t, history):
            text, labels = self.pd.repeated_prompt(variant, g, rounds, t, history, coop_first=False)
            return text, (lambda out: None if self.pd.parse_choice(out, labels) is None
                          else (game.endowment if self.pd.parse_choice(out, labels) else 0))

        def decide(seat, prompt, parse):
            seen.setdefault(seat, []).append(prompt)
            coop = plan[seat][calls[seat]]
            calls[seat] += 1
            out = '{"choice": "%s"}' % ("B" if coop else "A")           # coop_first=False: B is cooperation
            c = parse(out)
            return c, [{"valid": True, "attempt": 1, "contribution": c}]

        status, rows = play_game(g.engine, 3, ["llm", "llm"], "P0", decide, prompt_fn)
        self.assertEqual(status, "complete")
        for r in rows:
            own, other = plan[r["seat"]][r["round"] - 1], plan[1 - r["seat"]][r["round"] - 1]
            self.assertAlmostEqual(r["payoff"], g.payoff(own, other))
        self.assertIn("Round 1: you chose B, the other participant chose A, you received 14 points.", seen[0][1])
        self.assertIn("Round 1: you chose A, the other participant chose B, you received 34 points.", seen[1][1])
        self.assertIn("Round 2: you chose A, the other participant chose A, you received 20 points.", seen[0][2])
        text = self.pd.repeated_prompt("P0", g, 10, 1, [], True)[0].lower()
        for word in ("prison", "dilemma", "cooperat", "defect", "game", "team"):
            self.assertNotIn(word, text)


if __name__ == "__main__":
    unittest.main()
