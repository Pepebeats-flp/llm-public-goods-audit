# ODD description

Model: audit of LLM decision rules in the one-shot linear public goods game.
Protocol: ODD, second update (Grimm et al. 2020, JASSS 23(2) 7).
Implementation: `pgg/` in this repository. Version of 17 November 2026.

## 1. Purpose and patterns

**Purpose.** The model is an instrument for auditing a decision rule. It measures how an LLM, used as the decision rule of an agent, responds (a) to a change in a payoff parameter and (b) to a change in the wording of the task that leaves payoffs unchanged. Its purpose is description and exploration of the decision rule. It is not meant to predict human behaviour, to represent a population, or to evaluate policy, and no counterfactual conclusion is drawn from it.

**Patterns used to assess the decision rule.**

1. *Dominant action in the controls.* Outside the social dilemma the payoff-maximising action does not depend on the agent's disposition: contribute nothing when r < 1, contribute everything when r > N.
2. *Direction of the incentive response.* Human subjects contribute more when the marginal per capita return is higher; the one-shot Nash prediction is zero for every return below one.
3. *Invariance to payoff-equivalent rewording.* A decision rule that reflects the modelled incentives should give the same distribution of actions under descriptions that imply identical payoffs.

## 2. Entities, state variables and scales

**Agent.** One agent per observation. State variables:

| Variable | Values |
|---|---|
| `model` | identifier of the LLM (six models, see `configs/`) |
| `effort` | reasoning setting: `none` (off) or `high` (on) |
| `variant` | prompt variant: P0, P1, P2, P4, P3, F1, F2, F3 |
| `amount` | integer stated by the model, 0 to E |
| `contribution` | contribution implied by `amount` (E − amount under F1, else amount) |

**Environment.** State variables: number of players N = 4; endowment E = 20; multiplier r, set through the marginal per capita return m = r/N in {0.2, 0.3, 0.4, 0.5, 0.75, 1.25}. The derived variable `regime` is `control_inefficient` (r < 1), `dilemma` (1 < r < N) or `control_dominant` (r > N).

**Scales.** There is no space and no time. One observation is one decision in a game that is described as played once. The other N − 1 players exist only in the task description.

## 3. Process overview and scheduling

For each cell of the design (model × effort × m × variant × replicate):

1. The environment builds the task description for (N, E, r, variant) (`pgg/prompts.py`).
2. The description is sent to the model as a single user message in a fresh context (`pgg/llm.py`).
3. The model returns text. The environment extracts the last JSON object with an integer field `amount` in [0, E] (`parse_amount`). If there is none, the output is recorded as invalid and step 2 is repeated once; both rows are kept.
4. The environment maps `amount` to `contribution` and records the row (`pgg/run_oneshot.py`).

Cells are executed in a seeded random order, sequentially within a model, with a pause between calls. Comprehension probes follow the same steps with a question instead of a decision and are never placed in the same context as a decision. Payoffs are never computed by the model; when needed they are computed by `Game.payoffs` (`pgg/game.py`).

## 4. Design concepts

- **Basic principles.** The linear public goods game: u_i = E − c_i + (r/N) Σ_j c_j. The design rests on the distinction between the dilemma range, where self-interest and welfare conflict, and the two control ranges, where they coincide.
- **Emergence.** None. There is no interaction; outcomes are distributions of individual decisions.
- **Adaptation, objectives, learning, prediction.** Not modelled. The agent's rule is the LLM; no objective function is assigned to it and no explanation given by the model is treated as evidence of its rule.
- **Sensing.** The agent senses only the task description: N, E, r (or m in variant P2), the action space, simultaneity and the fact that the task happens once.
- **Interaction.** None between observations. Each call is independent.
- **Stochasticity.** Model sampling at temperature 1.0 is the only source of variation between replicates. The order of cells is shuffled with a fixed seed so that time is not confounded with condition.
- **Collectives.** None.
- **Observation.** For every call: prompt hash, returned text, reasoning trace if any, parsed amount, contribution, validity, token usage, latency, transport retries, served model identifier and timestamp (`data/raw/*.jsonl`).

## 5. Initialisation

Each call starts from an empty context. Parameters come from one configuration file per model and reasoning setting (`configs/final_*.json`): game size, list of m values, list of variants, replicates per cell (50), comprehension probes per cell, temperature, pacing and seed.

## 6. Input data

None. The model metadata recorded for documentation (`configs/opencode_go_models_snapshot.json`) is not used by the simulation.

## 7. Submodels

**7.1 Payoff rule.** `Game.payoffs(contributions)` returns E − c_i + r Σc / N for each player. `Game.dominant_action()` returns 0 if m < 1 and E if m > 1.

**7.2 Prompt variants.** All variants state the same rule; `tests/test_environment.py` checks, for random action profiles and all six values of m, that the payoff implied by the text of each variant equals the engine's payoff.

| Variant | Kind | What changes relative to P0 |
|---|---|---|
| P0 | baseline | neutral wording; no game name; avoids "public", "cooperate", "contribute", "game", "invest", "team", "group", "fair" |
| P1 | paraphrase | sentence order; unit "tokens" |
| P2 | paraphrase | return stated as what each participant receives per unit placed (m); unit "coins" |
| P4 | paraphrase | itemised layout |
| P3 | worked examples | P0 plus two examples: nobody and everybody placing the full endowment |
| F1 | framing | endowment starts in the shared account; the action is a withdrawal |
| F2 | framing | P0 preceded by "This task is called the Teamwork task." |
| F3 | framing | names the public goods game and uses its vocabulary (players, endowment, contribute, payoff) |

**7.3 Decision rule.** The LLM identified by `model`, called through an OpenAI-compatible chat-completions endpoint with `temperature` 1.0 and `reasoning_effort` set to `effort`. The model must answer with `{"amount": <integer from 0 to E>}`.

**7.4 Comprehension probes.** Two questions about the P0 rule with a numeric answer: the payoff of a player who places E while the others place 0 (correct: rE/N), and of a player who places 0 while the others place E (correct: E + r(N−1)E/N).

**7.5 Rule-based agents.** `pgg/agents.py` contains selfish, cooperative, reciprocal and adaptive agents and a repeated-game loop. They are used only in the environment tests; they are not part of the reported experiments.

## Addendum: repeated game (Study 2, part B)

**Scales and scheduling.** Groups of N = 4 agents play T = 10 rounds with a known horizon, E = 20 per round, m = 0.4. Within a round the agents decide in seat order, each without information about the current round. After the last agent has decided, the environment computes payoffs and appends to each agent's history its own contribution, the mean contribution of the other three and its payoff.

**Sensing and memory.** An agent senses the rules, the round number and its own history, all placed in one fresh prompt per decision (`repeated_prompt` in `pgg/prompts.py`). It has no other memory and does not see individual contributions of others. There is no communication.

**Interaction and collectives.** Agents interact only through the shared account. A group is homogeneous (four LLM agents of one model and wording) or mixed (three LLM agents and one rule-based agent that always contributes zero, `Selfish` in `pgg/agents.py`).

**Stochasticity.** Model sampling at temperature 1.0. The order of games is shuffled with a fixed seed.

**Observation.** One row per decision with round, seat, contribution, payoff, mean of the others and round total. A game is written only when it ends (`pgg/run_repeated.py`). A group is discarded if an agent returns two invalid outputs in a round; a game interrupted by a transport failure is not recorded and is played again.

## Addendum: prisoner's dilemma (Study 3)

**Entities and state variables.** Two agents per game. The environment is `PD(E, m)` in `pgg/pd.py` with E = 20 and m in {0.4, 0.6, 0.7, 0.8, 0.9, 1.25}. The action is binary. Payoffs are R = 2mE (both cooperate), T = E + mE, P = E (both defect) and S = mE, which are the payoffs of the public goods game with N = 2, r = 2m and a contribution of 0 or E. The regime is `dilemma` for 0.5 < m < 1, `control_inefficient` at m = 0.4 (defecting is dominant and efficient) and `control_dominant` at m = 1.25 (cooperating is dominant).

**Sensing.** The agent senses a description of the four outcomes with two option labels. The label that stands for cooperation alternates with the replicate (one-shot) or with the pair (repeated game) and is recorded as `coop_first`. The eight wordings parallel those of the public goods game (P0, P1, P2, P4, P3, F1, F2, F3). F3 names the prisoner's dilemma and uses the labels "cooperate" and "defect".

**Process.** As in sections 3 and the repeated-game addendum, with the answer format `{"choice": "<label>"}`. The choice is stored as `cooperate` and as a `contribution` of E or 0. In the repeated game (T = 10, m = 0.7) the history shows, for each past round, the agent's own choice, the other's choice and the agent's points. A pair is homogeneous (two LLM agents) or mixed (one LLM agent and a rule-based agent that always defects).

**Comprehension probes.** Two questions on the baseline description: the points of a participant who cooperates against a defector (S) and of one who defects against a cooperator (T).

## Verification

`python3 -m unittest discover -s tests` runs 27 tests covering the payoff rule, regimes and dominant actions (by enumeration), payoff equivalence of the variants, vocabulary of the neutral variants, answer keys of the probes, output parsing, reproducibility of the rule-based agents, and for the repeated game the prompts, the history shown to each agent, the recorded payoffs and the discard rules, and for the prisoner's dilemma the payoff order, dominance, payoff equivalence of the wordings under both label assignments, the parser and the repeated history.
