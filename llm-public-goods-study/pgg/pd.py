"""Prisoner's dilemma (Study 3).

Two players, binary action. The game is parameterised on the same incentive axis as the
public goods game: with endowment E and marginal return m, cooperating is contributing E
and defecting is contributing 0 in a two-player linear public goods game with r = 2m, so
payoffs are those of pgg.game.Game(2, E, 2m). In prisoner's dilemma notation:

    R = 2mE   both cooperate           T = E + mE   defect against a cooperator
    P = E     both defect              S = mE       cooperate against a defector

It is a prisoner's dilemma (T > R > P > S) when 0.5 < m < 1. For m < 0.5 defecting is
dominant and also efficient. For m > 1 cooperating is dominant and efficient.

The game is shown to the model as a table of four outcomes, not as a shared account.
Which label stands for cooperation is alternated by design (`coop_first`), so that a
preference for a letter or for the first option is not confounded with cooperation.

Every prompt builder returns (text, labels) where labels maps each admissible answer to
True (cooperate) or False (defect).
"""
from dataclasses import dataclass

from .game import Game
from .llm import parse_json_field


def _num(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


@dataclass(frozen=True)
class PD:
    endowment: int = 20
    mpcr: float = 0.7

    @property
    def n(self):
        return 2

    @property
    def r(self):
        return round(2 * self.mpcr, 6)

    @property
    def engine(self):
        return Game(2, self.endowment, self.r)

    @property
    def R(self):
        return 2 * self.mpcr * self.endowment

    @property
    def T(self):
        return self.endowment + self.mpcr * self.endowment

    @property
    def P(self):
        return float(self.endowment)

    @property
    def S(self):
        return self.mpcr * self.endowment

    @property
    def regime(self):
        if self.mpcr < 0.5:
            return "control_inefficient"   # defecting is dominant and efficient
        if self.mpcr > 1:
            return "control_dominant"      # cooperating is dominant and efficient
        if 0.5 < self.mpcr < 1:
            return "dilemma"
        return "boundary"

    def dominant_cooperates(self):
        if self.mpcr < 1:
            return False
        if self.mpcr > 1:
            return True
        return None

    def payoff(self, own_coop, other_coop):
        E = self.endowment
        return self.engine.payoffs([E if own_coop else 0, E if other_coop else 0])[0]


ANSWER_AB = 'Reply with only a JSON object of the form {"choice": "A"} or {"choice": "B"} and nothing else.'


def _answer_cd(first, second):
    return f'Reply with only a JSON object of the form {{"choice": "{first}"}} or {{"choice": "{second}"}} and nothing else.'


def _letters(coop_first):
    """(label of cooperation, label of defection, labels dict)."""
    c, d = ("A", "B") if coop_first else ("B", "A")
    return c, d, {c: True, d: False}


def _outcomes(g, c, d):
    """The four outcomes in the fixed order AA, BB, AB, BA as (own label, other label, own pay, other pay)."""
    pay = {(True, True): (g.R, g.R), (False, False): (g.P, g.P), (True, False): (g.S, g.T), (False, True): (g.T, g.S)}
    is_coop = {c: True, d: False}
    rows = []
    for own, other in (("A", "A"), ("B", "B"), ("A", "B"), ("B", "A")):
        a, b = pay[(is_coop[own], is_coop[other])]
        rows.append((own, other, _num(a), _num(b)))
    return rows


def _table_sentences(g, c, d, unit, other="the other participant"):
    out = []
    for own, oth, a, b in _outcomes(g, c, d):
        if own == oth:
            out.append(f"- If you both choose {own}, each of you receives {a} {unit}.")
        else:
            out.append(f"- If you choose {own} and {other} chooses {oth}, you receive {a} {unit} and {other} receives {b} {unit}.")
    return "\n".join(out)


def p0(g, coop_first=True):
    c, d, labels = _letters(coop_first)
    text = (
        "You are paired with one other participant in a task. Each of you privately chooses one of two options, A or B.\n"
        "The points each of you receives depend on both choices:\n"
        + _table_sentences(g, c, d, "points")
        + "\nBoth of you choose at the same time, without seeing the other's choice. The task happens only once.\n\n"
        "Which option do you choose?\n" + ANSWER_AB
    )
    return text, labels


def p1(g, coop_first=True):
    """Paraphrase: reordered sentences, unit 'tokens'."""
    c, d, labels = _letters(coop_first)
    text = (
        "This is a single-round task. It will not be repeated. You and one other participant decide simultaneously and in "
        "private, and neither sees the other's decision beforehand.\n"
        "There are two options, A and B, and each of you picks one. What each of you ends up with depends on the pair of picks:\n"
        + _table_sentences(g, c, d, "tokens")
        + "\n\nWhich option do you pick?\n" + ANSWER_AB
    )
    return text, labels


def p2(g, coop_first=True):
    """Paraphrase: outcomes listed as pairs, unit 'coins'."""
    c, d, labels = _letters(coop_first)
    lines = [f"- You {own}, other {oth}: {a} coins for you, {b} coins for the other." for own, oth, a, b in _outcomes(g, c, d)]
    text = (
        "You are taking part in a task with one other participant. Each of you privately selects option A or option B.\n"
        "The coins you both receive are set by the two selections together:\n"
        + "\n".join(lines)
        + "\nSelections are made at the same time and nobody sees the other's selection beforehand. This happens once only.\n\n"
        "Which option do you select?\n" + ANSWER_AB
    )
    return text, labels


def p4(g, coop_first=True):
    """Paraphrase: itemised layout."""
    c, d, labels = _letters(coop_first)
    lines = [f"  - you {own}, other {oth}: you {a}, other {b}" for own, oth, a, b in _outcomes(g, c, d)]
    text = (
        "Task description:\n"
        "- Participants: you and one other participant.\n"
        "- Decision: each participant picks option A or option B.\n"
        "- Points received, by pair of decisions:\n"
        + "\n".join(lines)
        + "\n- Timing: both decide simultaneously and privately. There is a single round.\n\n"
        "Which option do you pick?\n" + ANSWER_AB
    )
    return text, labels


def p3(g, coop_first=True):
    """P0 plus two worked examples giving the joint total of the two symmetric outcomes."""
    c, d, labels = _letters(coop_first)
    tot = {"A": _num(2 * (g.R if labels["A"] else g.P)), "B": _num(2 * (g.R if labels["B"] else g.P))}
    text = (
        "You are paired with one other participant in a task. Each of you privately chooses one of two options, A or B.\n"
        "The points each of you receives depend on both choices:\n"
        + _table_sentences(g, c, d, "points")
        + f"\nFor example, if you both choose A, the two of you receive {tot['A']} points in total. "
        f"If you both choose B, the two of you receive {tot['B']} points in total."
        "\nBoth of you choose at the same time, without seeing the other's choice. The task happens only once.\n\n"
        "Which option do you choose?\n" + ANSWER_AB
    )
    return text, labels


def _change(delta, target):
    return f"adds {_num(delta)} points to {target}" if delta >= 0 else f"removes {_num(-delta)} points from {target}"


def f1_take(g, coop_first=True):
    """Framing: both start at the both-cooperate outcome; one option takes from the other."""
    c, d, labels = _letters(coop_first)
    E, m = g.endowment, g.mpcr
    own, oth = E * (1 - m), -m * E          # effect of defecting on own and on the other's points
    effect = {c: "leaves the points of both participants as they are",
              d: f"{_change(own, 'your points')} and {_change(oth, 'the points of the other participant')}"}
    text = (
        f"You are paired with one other participant in a task. Each of you starts with {_num(g.R)} points.\n"
        "Each of you privately chooses one of two options, A or B.\n"
        f"- Option A {effect['A']}.\n"
        f"- Option B {effect['B']}.\n"
        "The other participant has the same two options, with the same effects seen from their side.\n"
        "Both of you choose at the same time, without seeing the other's choice. The task happens only once.\n\n"
        "Which option do you choose?\n" + ANSWER_AB
    )
    return text, labels


def f2_teamwork(g, coop_first=True):
    text, labels = p0(g, coop_first)
    return "This task is called the Teamwork task.\n" + text, labels


def f3_named(g, coop_first=True):
    """Framing: names the game and uses its vocabulary. `coop_first` sets the order of mention."""
    first, second = ("cooperate", "defect") if coop_first else ("defect", "cooperate")
    lines = {
        ("cooperate", "cooperate"): f"- If you both cooperate, each of you gets a payoff of {_num(g.R)}.",
        ("defect", "defect"): f"- If you both defect, each of you gets a payoff of {_num(g.P)}.",
        ("cooperate", "defect"): f"- If you cooperate and the other player defects, you get {_num(g.S)} and the other player gets {_num(g.T)}.",
        ("defect", "cooperate"): f"- If you defect and the other player cooperates, you get {_num(g.T)} and the other player gets {_num(g.S)}.",
    }
    order = [(first, first), (second, second), (first, second), (second, first)]
    text = (
        "You are playing a prisoner's dilemma with one other player. "
        f"Each of you privately chooses to {first} or to {second}.\n"
        "The payoffs are:\n" + "\n".join(lines[o] for o in order)
        + "\nBoth players decide at the same time, without seeing the other's decision. The game is played only once.\n\n"
        f"Do you {first} or {second}?\n" + _answer_cd(first, second)
    )
    return text, {"cooperate": True, "defect": False}


VARIANTS = {"P0": p0, "P1": p1, "P2": p2, "P4": p4, "P3": p3, "F1": f1_take, "F2": f2_teamwork, "F3": f3_named}
REPEATED_VARIANTS = ["P0", "F2", "F3"]


def parse_choice(text, labels):
    """True (cooperate), False (defect) or None if the output has no admissible choice."""
    v = parse_json_field(text, "choice")
    if not isinstance(v, str):
        return None
    v = v.strip()
    for key, coop in labels.items():
        if v.lower() == key.lower():
            return coop
    return None


def implied_payoff(variant, g, own_coop, other_coop):
    """Payoff implied by the text of each variant, written independently of the engine."""
    E, m = g.endowment, g.mpcr
    if variant == "F1":        # start at R; each defection adds E(1-m) to its author and removes mE from the other
        return g.R + (0 if own_coop else E * (1 - m)) - (0 if other_coop else m * E)
    table = {(True, True): g.R, (False, False): g.P, (True, False): g.S, (False, True): g.T}
    return table[(own_coop, other_coop)]


def comprehension_items(g, coop_first=True):
    """Two payoff questions about the P0 table, asked in separate calls."""
    c, d, _ = _letters(coop_first)
    rule = p0(g, coop_first)[0].split("\n\nWhich option")[0]
    tail = '\nReply with only a JSON object of the form {"answer": <number>} and nothing else.'
    q1 = rule + f"\n\nQuestion: suppose you choose {c} and the other participant chooses {d}. How many points do you receive?" + tail
    q2 = rule + f"\n\nQuestion: suppose you choose {d} and the other participant chooses {c}. How many points do you receive?" + tail
    return [("own_coop_other_defect", q1, g.S), ("own_defect_other_coop", q2, g.T)]


def repeated_prompt(variant, g, rounds, t, history, coop_first=True):
    """Prompt for round t of a repeated game. history: dicts with round, own, others_mean, payoff
    (own and others_mean are contributions, E for cooperation and 0 for defection)."""
    E = g.endowment
    if variant in ("P0", "F2"):
        c, d, labels = _letters(coop_first)
        name = {True: c, False: d}
        head = "This task is called the Teamwork task.\n" if variant == "F2" else ""
        if history:
            past = "Rounds played so far:\n" + "\n".join(
                f"Round {h['round']}: you chose {name[h['own'] == E]}, the other participant chose {name[h['others_mean'] == E]}, "
                f"you received {_num(round(h['payoff'], 2))} points." for h in history)
        else:
            past = "No rounds have been played yet."
        text = (
            head
            + f"You are paired with one other participant in a task that is repeated for {rounds} rounds with the same participant.\n"
            "In each round each of you privately chooses one of two options, A or B.\n"
            "The points each of you receives in a round depend on both choices:\n"
            + _table_sentences(g, c, d, "points")
            + "\nPoints from all rounds add up.\n"
            "Both of you choose at the same time, without seeing the other's choice for that round. "
            "After each round you are told the other participant's choice and your points for the round.\n\n"
            + past
            + f"\n\nThis is round {t} of {rounds}.\nWhich option do you choose in this round?\n" + ANSWER_AB
        )
        return text, labels
    if variant == "F3":
        first, second = ("cooperate", "defect") if coop_first else ("defect", "cooperate")
        word = {True: "cooperated", False: "defected"}
        lines = {
            ("cooperate", "cooperate"): f"- If you both cooperate, each of you gets a payoff of {_num(g.R)}.",
            ("defect", "defect"): f"- If you both defect, each of you gets a payoff of {_num(g.P)}.",
            ("cooperate", "defect"): f"- If you cooperate and the other player defects, you get {_num(g.S)} and the other player gets {_num(g.T)}.",
            ("defect", "cooperate"): f"- If you defect and the other player cooperates, you get {_num(g.T)} and the other player gets {_num(g.S)}.",
        }
        order = [(first, first), (second, second), (first, second), (second, first)]
        if history:
            past = "Rounds played so far:\n" + "\n".join(
                f"Round {h['round']}: you {word[h['own'] == E]}, the other player {word[h['others_mean'] == E]}, "
                f"your payoff was {_num(round(h['payoff'], 2))}." for h in history)
        else:
            past = "No rounds have been played yet."
        text = (
            f"You are playing a repeated prisoner's dilemma with one other player. The game lasts {rounds} rounds with the same player.\n"
            f"In each round each of you privately chooses to {first} or to {second}.\n"
            "The payoffs in a round are:\n" + "\n".join(lines[o] for o in order)
            + "\nPayoffs from all rounds add up.\n"
            "Both players decide at the same time, without seeing the other's decision for that round. "
            "After each round you are told the other player's decision and your payoff for the round.\n\n"
            + past
            + f"\n\nThis is round {t} of {rounds}.\nDo you {first} or {second} in this round?\n" + _answer_cd(first, second)
        )
        return text, {"cooperate": True, "defect": False}
    raise KeyError(variant)
