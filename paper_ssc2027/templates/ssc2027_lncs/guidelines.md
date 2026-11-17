# SSC 2027 Paper Writing Guidelines (working version)

Status: the SSC 2027 Call for Papers is not published yet (expected February 2027; submission deadline early April 2027). These guidelines follow the SSC 2026 (Durham) submission rules and the Springer LNCS author instructions. Re-check every item marked TBC when the 2027 call appears at https://essa.eu.org/ssc/2027/.

## Venue
* Social Simulation Conference 2027 (ESSA), Malmö University, 16-20 August 2027.
* Conference theme: "Social Simulation in Action: Catalysing Public Decision-Making?!"
* Target submission type: full paper intended for proceedings.
* Target track (TBC): the generative-AI / LLM track if one is offered (SSC 2026 had "Generative AI meets Agent-Based Modelling"); otherwise the general track.

## General Setup
* Document class: `\documentclass[runningheads]{llncs}` (Springer LNCS, llncs.cls v2.26).
* Bibliography style: `splncs04` (numeric citations with `\cite{}`).
* Do not change margins, fonts, or spacing of the class.
* Packages kept to a minimum: graphicx, amsmath, amssymb, booktabs, hyperref, xcolor.

## Paper Length
* Full paper: 6 to 12 pages in LNCS format. Whether references count toward the limit is TBC; plan for 12 pages including references.
* Extended abstract (fallback): 3 to 4 pages.

## Anonymity
* Checked 17 November 2026: neither the SSC 2026 submission page (Durham, via ConfTool) nor the SSC 2025 call mentions blind review or anonymised submissions. Author names are therefore included. Re-check when the 2027 call is published; if it asks for anonymous submissions, remove the author block, the repository URL and the acknowledgements.
* SSC 2025 stated page limits excluding references (long papers 10-12 pages, short papers 6-9); SSC 2026 stated 6-12 pages without saying whether references count.

## Originality
* Work must be original, not published and not under review elsewhere.

## Abstract and Keywords
* One paragraph, 150 to 250 words.
* `\keywords{}` with 3 to 5 keywords separated by `\and`.

## Structure expected by this community
* An explicit, replicable model description. Follow the ODD protocol (Grimm et al. 2020) in summary form in the paper; full ODD in the repository.
* State the modelling purpose explicitly (illustration, exploration, explanation, prediction).
* Justify assumptions; report sensitivity analysis and replications.
* Discuss validation: purpose alignment, external grounding, robustness.
* Discuss implications for modellers and, given the 2027 theme, for public decision-making.

## Citations and References
* Numeric: `\cite{key}`. Narrative use: "Li and Shirado~\cite{li2025spontaneous} report ...".
* Only cite entries present in `references.bib`. Every entry there has been checked against Scopus, Crossref, or the source itself.
* Never cite a number from a paper that was read only as an abstract without saying so in the working notes.

## Figures and Tables
* Figures: caption below. Tables: caption above. Use `booktabs` rules.
* All figures live in `figures/`; always include the `figures/` prefix in `\includegraphics`.
* Maximum 4 figures and 4 tables in the main text.
* Figures must be legible in greyscale.

## Numbers
* Every number in Results must come from `raw_materials/experimental_log.md`. No number is written before the experiment that produces it has run.
* Report means with 95% confidence intervals and effect sizes, with the game (not the agent) as the unit of analysis.

## Style
* British or American English, consistently. Plain, precise prose. Define every symbol on first use.
* Describe LLM behaviour through observed actions; do not attribute beliefs, intentions or preferences to the models.
* Name exact model identifiers, providers and query dates.

## Mandatory end matter
* Data and code availability statement with repository link (anonymised if required).
* Acknowledgements and disclosure of interests as required by Springer (`\begin{credits}`).
* Disclose use of generative AI tools. SSC pages state no rule of their own. Springer policy: language models cannot be authors; use of an LLM must be documented in the Methods section or a suitable alternative part of the manuscript; only AI-assisted copy editing of human-written text is exempt; authors remain accountable for the content.
