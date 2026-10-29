# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A university assignment deliverable, not a conventional application repo. The graded artifacts are **documents plus a deployed app**:

| Artifact | Role |
|---|---|
| `spec.md` | **Source of truth.** Problem, scope, architecture, the three scenarios verbatim, 10 acceptance criteria, the six Socratic rules, the eval protocol |
| `DESIGN.md` | Design tokens, four screens, Stitch prompts, production notes (§9) |
| `TUTOR-EVAL.md` | 20-session evaluation of the live tutor |
| `README.md` | Product decisions |
| `cypress/` | End-to-end tests |
| `calisma/` | Working files, **not delivered** |

Working language is **Turkish** for prose; code identifiers and the AI Studio build prompt are English.

## The app source is not in this repo

The application was built in Google AI Studio and is deployed at **<https://primer-1.ai.studio/>**. There is no buildable app source here.

- `uygulama/ai_studio_code.html` is an **early single-file export that diverges from production**. Production is a Vite bundle whose Socratic call goes to a same-origin server proxy; the export calls Gemini directly from the client. Do not treat the export as authoritative, and do not "fix" production by editing it.
- Changes to the app are made by prompting AI Studio and redeploying. `calisma/AI-STUDIO-PROMPT.md` holds the full build prompt; `calisma/ekran-markup.html` holds the reference screen markup extracted from the Stitch exports.

## Commands

```bash
npm install            # Cypress 16.x, ~10 min on first run (large binary)
npx cypress run        # all 13 tests, ~25s, records cypress/videos/
npx cypress open       # interactive runner
```

Cypress has no built-in test filter here. To run a single test, temporarily change `it(` to `it.only(` in `cypress/e2e/primer.cy.js`.

Tests run against the **production URL** (`baseUrl` in `cypress.config.js`), not a local server — production is what is graded. They stub `POST /api/socratic` via `cy.intercept`, both because assertions must check the app's contract rather than the model's wording, and because the live endpoint is rate limited.

## Architecture: the two-layer tutor

The app deliberately splits into two layers, and most invariants follow from this split:

| Layer | Implementation | Why |
|---|---|---|
| Branching — scenarios, options, endings | Hard-coded decision tree | Tests must see the same result every run |
| Socratic feedback | Live model call via the proxy | The eval needs real model behaviour to measure |

The proxy contract is `POST /api/socratic` with `{prompt}` returning `{text, fallback}`. When `fallback` is true or `text` is empty, the UI shows a fixed fallback question. That fallback is required, not cosmetic: the endpoint is rate limited and drops responses under rapid successive calls (measured in `TUTOR-EVAL.md` §4.3).

## Invariants that span multiple files

Changing any of these means changing every place listed, or the deliverables contradict each other.

**Scenario content and the ending rule.** The three scenarios' text, the 27 options and their `saglam`/`orta`/`riskli` tags, and the rule *at least 2 of 3 `saglam` → good ending* are mirrored in `spec.md` §5, the deployed app, `cypress/e2e/primer.cy.js`, and the eval harness. `spec.md` is the source; the others must follow it.

**Options must be indistinguishable — including their order.** No icon, checkmark, number, colour, badge or size difference, *and* the three options are shuffled on entry to each decision point. This is the product's only real claim — if the answer can be read off the screen, the app has no purpose. Identical styling alone was not enough: with a fixed order the `saglam` option was always first and a real user worked it out in three decisions (AC10, `TUTOR-EVAL.md` §4.4). Restated in `DESIGN.md` (İ2), the Stitch prompts (`DESIGN.md` §6) and the build prompt (`calisma/AI-STUDIO-PROMPT.md` §6.3).

Because of the shuffle, **tests must never select an option by `secenek-N` index** — they locate it by the option text defined in `spec.md` §5. The ids identify slots, not options.

**Simulation state is ephemeral; chat state is not.** The simulation keeps profile and decisions in memory only. The chat added in v2 stores `primer_user_email` and `primer_chat_<email>` in `localStorage` and posts `{email, message, history}` to `POST /api/chat`. The email is a **label, not an identity** — there is no password, no OAuth, and no per-user Gemini key anywhere in the bundle; everyone shares the same server-side quota. Different emails produce different answers because each carries its own conversation history. The UI must not claim more privacy than this: the profile note says "Simülasyon cevapların kaydedilmiyor", and the chat discloses what it stores.

**`<html lang="tr">`.** CSS `text-transform: uppercase` is locale aware; under `lang="en"` Turkish `i` becomes `I` instead of `İ`. This is acceptance criterion AC9 and is tested.

**`data-testid` contract.** The 15 test ids listed in `DESIGN.md` §9.5 are the test surface. `profil-sinif` / `profil-rol` / `profil-hedef` are *containers* — their inner buttons carry no ids, so tests select those by visible label.

**The six Socratic rules and the label taxonomy.** `spec.md` §6.1 defines S1–S6; §6.3 defines labels OK/A/F/E/B/C/D with severity order `A > F > E > B > C > D`. S1, S2 and S5 are machine-checkable; S3, S4 and S6 require human labelling. Both the forbidden-phrase list and the prompt that enforces the rules live in `spec.md` §6.1–6.2 and are copied into the build prompt — keep them in sync.

## Eval harness

The 20-combination eval runner is a throwaway script kept in the session scratchpad, not in this repo. Its protocol, combination design (A:7, B:7, C:6, each with ≥2 good and ≥2 bad endings) and output format are specified in `spec.md` §6.4, and raw runs are archived in `calisma/eval-ham.md` and `calisma/eval-ikinci-gecis.md`. Measure the **app's own endpoint**, not Gemini directly: the proxy decides the model and settings, so only the endpoint reflects what users actually receive.

## Model choice

`gemini-3.5-flash-lite`, chosen by measurement rather than preference: `gemini-3.8-flash` spent ~821 thinking tokens on a ~90-token answer and took 75–142 s, while the lite model answers in ~5.6 s with zero thinking tokens and equal rule compliance. `gemini-2.5-flash` returns 404 for new keys. Rationale is recorded in `spec.md` §9.

## Not a git repository

There is no `.git` here. If version control is wanted, initialise it rather than assuming history exists.
