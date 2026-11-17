"""Prompt variants for the one-shot game.

Every variant describes the same payoff rule. P0, P1, P2 and P4 are paraphrases (same
information, different wording). P3 adds worked examples. F1-F3 are framings (different
scenario, same payoffs).

Each builder returns (prompt_text, to_contribution) where to_contribution maps the integer
the model answers ("amount") to the contribution c in [0, E] used by the game engine.
`implied_payoff` gives the payoff the text of each variant implies, as an independent
formula, so tests can check payoff equivalence against the engine.
"""

ANSWER = 'Reply with only a JSON object of the form {{"amount": <integer from 0 to {E}>}} and nothing else.'


def _num(x):
    """Format numbers without trailing zeros (1.6 -> '1.6', 2.0 -> '2')."""
    return f"{x:.4f}".rstrip("0").rstrip(".")


def p0(g):
    n, E, r = g.n, g.endowment, _num(g.r)
    text = (
        f"You are one of {n} participants in a task. Each participant starts with {E} points.\n"
        f"Each participant privately chooses a whole number of points, from 0 to {E}, to place in a shared account, "
        f"and keeps the rest.\n"
        f"The total placed in the shared account is multiplied by {r} and then divided equally among all {n} participants, "
        f"whatever each one placed.\n"
        f"Your final points are the points you kept plus your share of the shared account.\n"
        f"All participants choose at the same time, without seeing the others' choices. The task happens only once.\n\n"
        f"How many points do you place in the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


def p1(g):
    """Paraphrase: reordered sentences, unit 'tokens'."""
    n, E, r = g.n, g.endowment, _num(g.r)
    text = (
        f"This is a single-round task; it will not be repeated. There are {n} participants, including you, "
        f"and everyone decides simultaneously and in private.\n"
        f"What you end up with is whatever you keep plus an equal share of a shared account. "
        f"The shared account is filled by the participants: its total is multiplied by {r} before being split "
        f"into {n} equal parts, one per participant, regardless of who put in what.\n"
        f"You and every other participant begin with {E} tokens and decide how many of them (a whole number between 0 and {E}) "
        f"go into the shared account. The tokens you do not put in stay with you.\n\n"
        f"How many tokens do you put into the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


def p2(g):
    """Paraphrase: return expressed per unit placed, unit 'coins'."""
    n, E, m = g.n, g.endowment, _num(g.mpcr)
    text = (
        f"You are taking part in a task with {n - 1} other participants ({n} in total). Everyone starts with {E} coins.\n"
        f"Each participant privately picks a whole number of coins, from 0 to {E}, to move into a shared account. "
        f"Coins not moved are kept.\n"
        f"For every coin that any participant moves into the shared account, each of the {n} participants receives {m} coins, "
        f"no matter who moved it.\n"
        f"Your final coins are the coins you kept plus what you receive from the shared account.\n"
        f"Choices are made at the same time and nobody sees the others' choices beforehand. This happens once only.\n\n"
        f"How many coins do you move into the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


def p3(g):
    """P0 wording plus two worked examples at the extremes.

    Classified as 'example', not as a pure paraphrase: the examples add no payoff
    information but display the all-contribute outcome, and the pilot showed a large shift.
    """
    n, E, r = g.n, g.endowment, _num(g.r)
    each_full = _num(g.r * E)
    text = (
        f"You are one of {n} participants in a task. Each participant starts with {E} points.\n"
        f"Each participant privately chooses a whole number of points, from 0 to {E}, to place in a shared account, "
        f"and keeps the rest.\n"
        f"The total placed in the shared account is multiplied by {r} and then divided equally among all {n} participants, "
        f"whatever each one placed.\n"
        f"For example, if nobody places anything, the shared account is empty and each participant ends with {E} points. "
        f"If all {n} participants place all {E} points, the shared account holds {n * E} points, which become "
        f"{_num(g.r * n * E)}, and each participant ends with {each_full} points.\n"
        f"Your final points are the points you kept plus your share of the shared account.\n"
        f"All participants choose at the same time, without seeing the others' choices. The task happens only once.\n\n"
        f"How many points do you place in the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


def p4(g):
    """Paraphrase: itemised layout, unit 'points'. Same information as P0."""
    n, E, r = g.n, g.endowment, _num(g.r)
    text = (
        f"Task description:\n"
        f"- Participants: {n}, and you are one of them.\n"
        f"- Starting amount: {E} points each.\n"
        f"- Decision: every participant picks a whole number from 0 to {E}. That many points go into a shared account; "
        f"the remaining points stay with that participant.\n"
        f"- Shared account: its total is multiplied by {r}, then split into {n} equal parts, one for each participant, "
        f"independently of how many points each one put in.\n"
        f"- Result for you: the points that stayed with you, plus your part of the shared account.\n"
        f"- Timing: everyone decides simultaneously and privately. There is a single round.\n\n"
        f"How many points do you put into the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


def f1_take(g):
    """Framing: endowment starts in the shared account; the agent chooses a withdrawal."""
    n, E, r = g.n, g.endowment, _num(g.r)
    text = (
        f"You are one of {n} participants in a task. A shared account starts with {n * E} points, {E} for each participant.\n"
        f"Each participant privately chooses a whole number of points, from 0 to {E}, to withdraw from the shared account "
        f"for themselves.\n"
        f"The points left in the shared account after all withdrawals are multiplied by {r} and then divided equally "
        f"among all {n} participants, whatever each one withdrew.\n"
        f"Your final points are the points you withdrew plus your share of the shared account.\n"
        f"All participants choose at the same time, without seeing the others' choices. The task happens only once.\n\n"
        f"How many points do you withdraw from the shared account?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: g.endowment - a)


def f2_teamwork(g):
    """Framing: community label, same rules as P0."""
    base, conv = p0(g)
    return "This task is called the Teamwork task.\n" + base, conv


def f3_named(g):
    """Framing: names the game and uses its usual vocabulary."""
    n, E, r = g.n, g.endowment, _num(g.r)
    text = (
        f"You are playing a public goods game with {n - 1} other players ({n} in total). Each player has an endowment of {E} points.\n"
        f"Each player privately decides how many points, a whole number from 0 to {E}, to contribute to the public good, "
        f"and keeps the rest.\n"
        f"Total contributions are multiplied by {r} and then divided equally among all {n} players, "
        f"whatever each one contributed.\n"
        f"Your payoff is the points you kept plus your share of the public good.\n"
        f"All players decide at the same time, without seeing the others' contributions. The game is played only once.\n\n"
        f"How many points do you contribute to the public good?\n" + ANSWER.format(E=E)
    )
    return text, (lambda a: a)


VARIANTS = {
    "P0": p0, "P1": p1, "P2": p2, "P4": p4, "P3": p3,
    "F1": f1_take, "F2": f2_teamwork, "F3": f3_named,
}
KIND = {"P0": "baseline", "P1": "paraphrase", "P2": "paraphrase", "P4": "paraphrase", "P3": "example",
        "F1": "framing", "F2": "framing", "F3": "framing"}
PARAPHRASE_SET = ["P0", "P1", "P2", "P4"]   # same information, different wording
FRAMING_SET = ["P0", "F1", "F2", "F3"]      # baseline against each framing


def implied_payoff(variant, g, own_answer, others_answers):
    """Payoff implied by the *text* of each variant, written independently of the engine."""
    n, E = g.n, g.endowment
    answers = [own_answer] + list(others_answers)
    if variant in ("P0", "P1", "P3", "P4", "F2", "F3"):
        return (E - own_answer) + g.r * sum(answers) / n
    if variant == "P2":   # each unit moved by anyone pays m to everyone
        return (E - own_answer) + g.mpcr * sum(answers)
    if variant == "F1":   # answers are withdrawals from an account that starts at n*E
        return own_answer + g.r * (n * E - sum(answers)) / n
    raise KeyError(variant)


def comprehension_items(g):
    """Two payoff-calculation questions about the P0 rule, with correct answers.

    Asked in separate calls, never in the same context as a decision, so that answering
    them cannot influence the decision.
    """
    n, E, r = g.n, g.endowment, g.r
    rule, _ = p0(g)
    rule = rule.split("\n\nHow many")[0]
    q1 = (rule + f"\n\nQuestion: suppose you place {E} points in the shared account and each of the other "
          f"{n - 1} participants places 0. How many points do you end with?\n"
          'Reply with only a JSON object of the form {"answer": <number>} and nothing else.')
    a1 = r * E / n
    q2 = (rule + f"\n\nQuestion: suppose you place 0 points in the shared account and each of the other "
          f"{n - 1} participants places {E}. How many points do you end with?\n"
          'Reply with only a JSON object of the form {"answer": <number>} and nothing else.')
    a2 = E + r * (n - 1) * E / n
    return [("own_full_others_zero", q1, a1), ("own_zero_others_full", q2, a2)]


# ---------------------------------------------------------------------------------------
# Repeated game (Study 2). Same payoff rule each round; the prompt is rebuilt every round
# from the rules and the history, so a call carries no chat memory.
# ---------------------------------------------------------------------------------------

REPEATED_VARIANTS = ["P0", "F2", "F3"]


def _history_lines(history, unit, placed, received):
    """history: list of dicts with keys round, own, others_mean, payoff (one per past round)."""
    if not history:
        return "No rounds have been played yet."
    lines = ["Rounds played so far:"]
    for h in history:
        lines.append(
            f"Round {h['round']}: you {placed} {h['own']}, the others {placed} {_num(round(h['others_mean'], 1))} "
            f"on average, you {received} {_num(round(h['payoff'], 2))} {unit}."
        )
    return "\n".join(lines)


def repeated_prompt(variant, g, rounds, t, history):
    """Prompt for round t (1-based) of a game of `rounds` rounds. Returns (text, to_contribution)."""
    n, E, r = g.n, g.endowment, _num(g.r)
    if variant in ("P0", "F2"):
        head = "This task is called the Teamwork task.\n" if variant == "F2" else ""
        text = (
            head
            + f"You are one of {n} participants in a task that is repeated for {rounds} rounds with the same participants.\n"
            f"At the start of every round each participant receives {E} points.\n"
            f"In each round each participant privately chooses a whole number of points, from 0 to {E}, to place in a "
            f"shared account, and keeps the rest.\n"
            f"The total placed in the shared account in a round is multiplied by {r} and then divided equally among all "
            f"{n} participants, whatever each one placed.\n"
            f"Your points for a round are the points you kept plus your share of the shared account. "
            f"Points from all rounds add up.\n"
            f"All participants choose at the same time, without seeing the others' choices for that round. "
            f"After each round you are told the average placed by the other participants and your points for the round.\n\n"
            + _history_lines(history, "points", "placed", "received")
            + f"\n\nThis is round {t} of {rounds}.\n"
            f"How many points do you place in the shared account in this round?\n" + ANSWER.format(E=E)
        )
    elif variant == "F3":
        text = (
            f"You are playing a repeated public goods game with {n - 1} other players ({n} in total). "
            f"The game lasts {rounds} rounds with the same players.\n"
            f"At the start of every round each player has an endowment of {E} points.\n"
            f"In each round each player privately decides how many points, a whole number from 0 to {E}, to contribute "
            f"to the public good, and keeps the rest.\n"
            f"Total contributions in a round are multiplied by {r} and then divided equally among all {n} players, "
            f"whatever each one contributed.\n"
            f"Your payoff for a round is the points you kept plus your share of the public good. "
            f"Payoffs from all rounds add up.\n"
            f"All players decide at the same time, without seeing the others' contributions for that round. "
            f"After each round you are told the average contribution of the other players and your payoff for the round.\n\n"
            + _history_lines(history, "points", "contributed", "received")
            + f"\n\nThis is round {t} of {rounds}.\n"
            f"How many points do you contribute to the public good in this round?\n" + ANSWER.format(E=E)
        )
    else:
        raise KeyError(variant)
    return text, (lambda a: a)
