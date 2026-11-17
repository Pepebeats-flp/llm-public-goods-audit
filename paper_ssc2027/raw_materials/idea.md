# idea.md — dense idea for the SSC 2027 paper

Working title: **Nash's Players or Smith's Moral Agents? Auditing LLM Decision Rules in Public Goods Games**
Alternative: **Incentives or Wording? Auditing LLM Agents as Decision Rules in Public Goods Games**

> **Scope actually executed (17 November 2026).** Only the one-shot game was run: E0, E1, E2 and a reasoning arm. Final design: 8 prompt variants (paraphrases P0, P1, P2, P4; worked examples P3, reclassified after the pilot; framings F1, F2, F3), 6 models through OpenCode Go (gpt-5.6-luna, claude-haiku-5-5, qwen3.8-flash, glm-5.3-flash, deepseek-v4.1-flash, hy3), 50 decisions per cell, comprehension probes in separate calls. Rule-based agents, mixed populations, the repeated game and the strategy method (E3, E4) were not run and are future work. The paper title became "Incentives or Wording? Auditing LLM Decision Rules in a Public Goods Game". The authoritative description is `../preregistration.md`; results are in `experimental_log.md`. The text below is the original plan.

## Problem Statement

Large language models (LLMs) are increasingly used as the decision rule of agents in agent-based models (ABMs). The social simulation community has identified validation as the central open problem of this practice: output plausibility, clever prompting or calibration do not show that an LLM behaves reliably for a modelling purpose. Two things must hold before an LLM can stand in for a behavioural rule:

1. **Incentive responsiveness.** When the modeller changes a payoff parameter, the agent's action must change in a direction that some stated theory or body of evidence predicts.
2. **Wording invariance.** When the modeller rewrites the description of the same situation without changing its payoffs, the action should not change, or the change should be small relative to the effect of incentives.

Existing studies of LLMs in social dilemmas do not test these two properties together in an N-player game. Studies of LLMs in public goods games use a single payoff configuration and a single, context-laden prompt, or sweep the multiplier for one older model with one run per variant. Studies of framing change the content of the scenario rather than only its wording, so they cannot separate paraphrase noise from framing effects.

## Purpose of the model (ODD "purpose")

Exploration and audit, not prediction. The paper measures properties of LLM decision rules in a controlled game. It does not claim that LLM agents represent human populations and it draws no counterfactual policy conclusions from LLM societies. On the Mechanism Plausibility Scale of Zhao et al. the work sits at level 1 (reproducible phenomenal model with an operationalised target) with elements of level 2 (falsifiable hypotheses).

## Conceptual framing

In the one-shot linear public goods game three reference predictions are available:

* **Nash equilibrium:** zero contribution is a dominant strategy when the marginal per capita return is below one.
* **Adam Smith, Wealth of Nations, Book V, ch. i, part III:** public works "though they may be in the highest degree advantageous to a great society, are, however, of such a nature that the profit could never repay the expence to any individual", so individuals cannot be expected to provide them. In this game Smith and Nash agree.
* **Adam Smith, Theory of Moral Sentiments, opening sentence:** "How selfish soever man may be supposed, there are evidently some principles in his nature, which interest him in the fortune of others". This suggests positive voluntary contributions.
* **Human laboratory evidence:** initial contributions of 40 to 60 percent of the endowment, increasing in the marginal per capita return, declining with repetition, with roughly half of subjects conditional cooperators and about a quarter free riders.

The question is which of these the LLM agents resemble, and whether the answer depends on incentives or on wording. The framing is used in the Introduction and Discussion only. The mapping from the Theory of Moral Sentiments to positive contributions in public goods games is our interpretation. "Nash versus Smith" as a contradiction is historically wrong and must not be claimed.

Link to the conference theme (public decision-making): if LLM agents contribute far more than humans by default, a simulation populated with them makes the public good appear to provide itself, and understates the need for the institutions Smith assigned to the sovereign.

## Formal model

Linear public goods game. N agents, each with endowment E, choose a contribution c_i in {0, 1, ..., E}. The pool is multiplied by r and shared equally.

* Payoff (Eq. 1): u_i(c_i, c_-i) = E - c_i + (r/N) * sum_j c_j
* Marginal per capita return (MPCR): m = r/N
* Welfare (Eq. 2): W(c) = sum_i u_i = N*E + (r - 1) * sum_i c_i
* Social dilemma range: 1 < r < N, i.e. 1/N < m < 1. Zero contribution is dominant; full contribution maximises welfare.
* Out-of-dilemma controls: (a) r < 1: zero contribution is both dominant and welfare-maximising; (b) r > N (m > 1): full contribution is both dominant and welfare-maximising. In both controls self-interest and collective welfare coincide, so any agent that processes the payoff rule should choose the same action. They serve as comprehension tests and as a guard against recitation of the textbook answer, which is wrong in these conditions.
* Normalised efficiency (Eq. 3): (W - W_Nash) / (W_opt - W_Nash). In the linear game inside the dilemma this equals the mean normalised contribution.
* One-shot unilateral regret: Regret_i = c_i * (1 - r/N). It is a rescaling of the contribution and is not reported as a separate metric.

Repeated game: the same group plays T rounds with a known horizon; after each round every agent observes its own payoff and the mean contribution of the others. The one-shot equilibrium is used only as a static reference.

## Baseline parameters (anchored in the literature)

* N = 4, E = 20, integer contributions.
* MPCR inside the dilemma: 0.3, 0.4, 0.5, 0.75. (0.3 and 0.75 match Isaac and Walker 1988; 0.4 matches Fischbacher and Gächter 2010 and Sreedhar et al. 2025 with N = 4; 0.5 matches Li and Shirado 2025 and Mei et al. 2024.)
* Controls: m = 0.2 (r = 0.8) and m = 1.25 (r = 5).
* Secondary condition: N = 10, E = 20, r = 2 (m = 0.2), 20 rounds, to replicate the γ-Bench configuration.

## Agents

* **Selfish:** c_i = 0.
* **Cooperative:** c_i = E.
* **Reciprocal:** contributes the rounded mean contribution of the others in the previous round; E/2 in round 1.
* **Adaptive:** non-linguistic learner; exponential moving average of own payoffs per action (epsilon-greedy bandit over a coarse action grid).
* **LLM:** receives the rules and permitted observations and returns a JSON object {"contribution": <int>}. The game engine validates the action and computes all payoffs. Unparseable outputs are recorded as invalid and handled by a rule fixed before the experiment (one retry, then exclusion with reporting). The textual explanation of the LLM is never used as evidence.

LLM set (to be fixed after the pilot): two or three model families, at least one open-weight model run locally; exact identifiers, providers, dates, temperature and reasoning mode recorded. For at least one family both the reasoning and the non-reasoning variant are run.

## Prompt conditions

All variants describe the same payoff rule and are checked automatically for payoff equivalence.

* **P0 neutral baseline:** does not name the game; avoids "public", "cooperate", "contribute"; uses "points", "other participants", "shared account".
* **P1–P3 paraphrases (same information):** reordered sentences; different payoff unit (points, tokens, coins); return expressed as multiplier, as share received per point placed, or with a worked numeric example.
* **F1 take frame:** the endowment starts in the shared account and the agent decides how much to withdraw (Andreoni 1995).
* **F2 community label:** the task is called "Teamwork" (Sreedhar et al. 2025).
* **F3 named game:** the prompt states that this is a public goods game (as in Mei et al. 2024); measures the effect of triggering recalled literature.

## Experiments

* **E0 Environment validation.** Deterministic policies; payoff, equilibrium, optimum and seed reproducibility checks. Not hypothesis-testing.
* **E1 Incentive-response curve (RQ1).** One-shot game; sweep m over the four dilemma values and two controls; P0 prompt; each LLM. Before deciding, the agent answers two payoff-calculation questions; the accuracy is reported separately.
* **E2 Paraphrase versus framing (RQ2).** One-shot; full factorial m × prompt variant (P0–P3, F1–F3) × model.
* **E3 Population composition (RQ3).** Repeated game, m = 0.4: homogeneous LLM groups, mixed-LLM groups, and LLM agents mixed with selfish, cooperative and reciprocal rule agents in different proportions.
* **E4 Conditional cooperation and repetition (RQ4).** (a) Strategy method: the agent states a contribution for every possible rounded mean contribution of the others (0 to 20), following Fischbacher, Gächter and Fehr (2001); (b) repeated game, T = 10, homogeneous groups.
* **E5 Robustness.** Seeds, agent order, temperature, and where available a second version of the same model.

Minimum viable paper: E0, E1 and E2 with two models.

## Research questions and hypotheses (to be preregistered before the final run)

* RQ1 incentives. H1a: mean contribution increases with m inside the dilemma (direction from human evidence, not from Nash). H1b: in the controls, contributions are near E when m > 1 and near 0 when r < 1; deviations indicate failure to process the payoff rule.
* RQ2 prompt. H2: dispersion across paraphrases is greater than zero and smaller than dispersion across framings.
* RQ3 composition. H3: mixed societies differ from homogeneous ones in welfare and inequality; more cooperative agents earn less when mixed with selfish agents.
* RQ4 repetition. H4: contributions depend positively on the observed mean contribution of others.
* H5 exploratory: reasoning variants contribute less than non-reasoning variants across m (extends Li and Shirado 2025).

## Metrics

* Mean normalised contribution; welfare; Gini of cumulative payoffs; mean payoff by agent type.
* Incentive response: slope of contribution on m inside the dilemma; Spearman monotonicity; error in the two controls; comprehension accuracy; comparison with human slopes.
* Prompt consistency: standard deviation of mean contribution across paraphrases at fixed m and model; framing effect sizes; variance decomposition across incentive, paraphrase, framing, model and seed (mixed model with variance components; dominance analysis as in Lorè and Heydari 2024 as a robustness check).
* **Signal-to-noise ratio (headline number per model):** variance explained by the incentive divided by variance explained by paraphrase.
* Repeated game: conditional-cooperation slope and type classification from the strategy method; decay per round; end-game effect.
* Heterogeneity and operation: between-agent standard deviation within condition; between-seed variance; invalid-action rate; token cost.

## Statistical analysis

Game as the unit of analysis; bootstrap by game or hierarchical models; mixed models with random effects for game and agent in the repeated game; correction for multiple comparisons; effect sizes and intervals. Contributions of LLMs tend to cluster on a few values, so distributions are inspected before choosing models (ordinal or fractional regression if needed).

## Core contributions

1. A reproducible audit protocol for LLM decision rules in the linear public goods game, documented with ODD, with payoff-equivalent prompt variants.
2. Incentive-response curves for current models, with out-of-dilemma controls and comparison with human stylised facts and the Nash prediction.
3. A decomposition of contribution variance into incentive, paraphrase, framing, model and seed components, summarised as a signal-to-noise ratio per model.
4. Collective outcomes (welfare, inequality) in homogeneous and mixed populations.
5. Open artefacts: code, prompts, configurations, model versions, seeds and raw data.

## Positioning against the closest prior work

* **Huang et al. (γ-Bench, ICLR 2025):** closest antecedent. Public goods game with N = 10, 20 tokens, multiplier 2, 20 rounds. For GPT-3.5 only: sweep of the multiplier over 0, 0.5, 1, 2, 4 (never reaching m > 1), five prompt templates with one run each, one fixed free rider among nine LLM agents. No variance decomposition, no mixed models, no human comparison.
* **Li and Shirado (EMNLP 2025):** N = 4, 100 points, multiplier 2, binary action, one prompt ("group project"). Reasoning variants cooperate far less than non-reasoning ones.
* **Sreedhar et al. (IUI 2025):** gpt-4o-mini only, multiplier 1.6, five games per condition; game name and priming change contributions strongly; the authors name the fixed multiplier as a limitation.
* **Mei et al. (PNAS 2024):** N = 4, $20, m = 0.5, scripted co-players, prompt names the game and frames it as a water cleaning project; chatbots never contribute zero.
* **Pal et al. (PNAS Nexus 2026):** repeated prisoner's dilemma; neutral labelling; parameter adaptation and nine goal framings; consistency judged qualitatively.

## Threats to validity to be addressed in the text

Training-data contamination (the game is classic); confusion between comprehension and preference; over-control by prompt; anthropomorphism; stochasticity; dependence between agents; API drift; reasoning mode; position and label bias; external validity; comparison with human data from different designs (directions and orders of magnitude only).
