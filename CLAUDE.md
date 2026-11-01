# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A university assignment deliverable, not a conventional application repo. The graded artifacts are **documents plus a deployed app**:

| Artifact | Role |
|---|---|
| `spec.md` | **Source of truth.** Problem, scope, architecture, the three scenarios verbatim, **13 acceptance criteria**, the six Socratic rules, the eval protocol, **§10 model requirement** |
| `DESIGN.md` | Design tokens, four screens, Stitch prompts, production notes (§9) |
| `TUTOR-EVAL.md` | 20-session evaluation of the live tutor |
| `README.md` | Product decisions |
| `cypress/` | End-to-end tests |
| `calisma/` | Working files, **not delivered** |
| **`DEVAM.md`** | **Read this first.** Current state, what is pending, exact resume commands |

## v2 (assignment 2): the model layer

A second assignment (due 2026-11-06) added a small vertical model on top of v1. `DEVAM.md` holds live state; this section holds the parts that do not change.

| Artifact | Role |
|---|---|
| `sozlesme.py` | **Single source of truth** for column names, feature order, label rule, thresholds. `data/veri_derle.py`, `train.py` and `tests/parite.py` all import it — three copies of one threshold is how train/serve skew starts |
| `train.py` | One command, seed 42, grouped CV, **eval gate**, ONNX export |
| `data/` | `SOZLUK.md` (data dictionary), `veri_derle.py` (merge + validate), `ham/` (raw downloads), `oturumlar.csv` (derived, regenerated) |
| `model/` | `model.onnx` (553 B) · `config.json` (the contract) · `README.md` (model card) |
| `web/` | `index.html` — the v2 app · `site.json` — deployment config |
| `tests/parite.py` + `parite.json` | Test oracle for the differential test |
| `RELEASE.md` | Trade-off matrix, shadow/canary/rollback |
| `SINAV_TASARIMI.md` | Exam-design thought exercise |

Working language is **Turkish** for prose; code identifiers and the AI Studio build prompt are English.

## Two apps, two origins

| App | Where | Source in repo? | Carries |
|---|---|---|---|
| **v1** | <https://primer-1.ai.studio/> (AI Studio) | **no** | Live Socratic feedback via same-origin proxy |
| **v2** | <https://gonulnazire.github.io/primer/web/> (GitHub Pages) | **yes** — `web/index.html` | The model layer (`onnxruntime-web`), data collection |

The split is forced by a measured constraint, not preference: `OPTIONS https://primer-1.ai.studio/api/socratic` returns **no `Access-Control-Allow-Origin`**, so a page on any other origin cannot call the Socratic endpoint. v2 therefore shows the fixed fallback question and says so on screen. Full reasoning: `RELEASE.md` §2.

Do not "fix" this by making v2 call the v1 endpoint — it cannot work from the browser.

## The v1 app source is not in this repo

The v1 application was built in Google AI Studio and is deployed at **<https://primer-1.ai.studio/>**. There is no buildable v1 app source here.

- `uygulama/ai_studio_code.html` is an **early single-file export that diverges from production**. Production is a Vite bundle whose Socratic call goes to a same-origin server proxy; the export calls Gemini directly from the client. Do not treat the export as authoritative, and do not "fix" production by editing it.
- Changes to the app are made by prompting AI Studio and redeploying. `calisma/AI-STUDIO-PROMPT.md` holds the full build prompt; `calisma/ekran-markup.html` holds the reference screen markup extracted from the Stitch exports.

## Commands

```bash
npm install            # Cypress 16.x, ~10 min on first run (large binary)
npx cypress run        # all 34 tests (4 specs), ~60s, records cypress/videos/
npx cypress open       # interactive runner

# v2 model side (Python 3.14 venv already set up as .venv)
.venv/Scripts/python.exe data/veri_derle.py --sentetik 20   # merge + validate data
.venv/Scripts/python.exe train.py                           # train, eval gate, export ONNX
.venv/Scripts/python.exe train.py --esik 0.99               # prove the gate blocks (exit 2)
.venv/Scripts/python.exe tests/parite.py                    # oracle self-check
.venv/Scripts/python.exe tests/parite.py --yaz              # refresh after retraining
npm run v2                                                  # local static server :4173
```

Cypress has no built-in test filter here. To run a single test, temporarily change `it(` to `it.only(` in `cypress/e2e/primer.cy.js`.

**Never run `cypress run --spec <subset>` when you care about the videos.** Cypress empties `videosFolder` before every run, so a subset run deletes the committed videos of the specs it did not run. Recover with `git checkout -- cypress/videos/`. (`trashAssetsBeforeRuns: false` was tried and reverted — it writes `name (1).mp4` copies instead of overwriting, so the tracked videos go stale.)

v2 specs target `Cypress.expose('v2Url')`, not `baseUrl`. Cypress 16 removed `Cypress.env()`; config key is `expose`, CLI flag is `-x`.

Tests run against the **production URL** (`baseUrl` in `cypress.config.js`), not a local server — production is what is graded. They stub `POST /api/socratic` via `cy.intercept`, both because assertions must check the app's contract rather than the model's wording, and because the live endpoint is rate limited.

## Architecture: three layers

The app deliberately splits into layers, and most invariants follow from this split:

| Layer | Implementation | Why |
|---|---|---|
| Branching — scenarios, options, endings | Hard-coded decision tree | Tests must see the same result every run |
| Socratic feedback | Live model call via the proxy (**v1 only**) | The eval needs real model behaviour to measure |
| **Adaptation (v2)** | Our own logistic regression, ONNX in the browser | Learning from behaviour must be a measurable, versionable, revertable artifact |

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

## v2 invariants

These span files the same way the v1 ones do; breaking one makes the deliverables contradict each other.

**The model may say *when to pause*, never *what to choose*.** Its only action is the reflection pause, and that pause must not name, highlight or reorder any option. This follows directly from the product's single claim (`spec.md` §1, §6.1 S1) — a model that could hint would destroy it. Stated in `spec.md` §10.2, enforced by AC13 in `cypress/e2e/v2-akis.cy.js` (the pause text must not contain any option's text), and repeated in `model/README.md` §2.

**Feature order is the contract.** `sozlesme.py` → `OZELLIKLER`, `model/config.json` → `girdi.ozellikler`, `tests/parite.json` → `ozellikler`, and the `OZELLIKLER` array in `web/index.html` must all match, in order. A parity test still passes if they drift together — it would just be answering a different question. `cypress/e2e/parite.cy.js` checks two of these against each other.

**Two thresholds, never conflated.** Eval gate **0.70** (grouped out-of-fold ROC-AUC, decides whether the model may be published) vs action threshold **0.60** (probability, decides whether the app intervenes). `spec.md` §10.5.

**The eval gate is not negotiable after the fact.** The threshold was written before any data existed. If a retrain falls below it, collect more data — do not lower the gate. Reporting an honest failure scores better than a quiet adjustment (the assignment says so explicitly).

**The label rule is frozen.** `refleks = okuma_orani < 0.4`, defined in `sozlesme.py` and `spec.md` §10.4 before collection. Changing it after seeing data means fitting the label to the model.

**v1 spec files stay byte-identical.** `cypress/e2e/primer.cy.js` and `sohbet.cy.js` must not be edited — the regression evidence is worth more than the ~30 duplicated helper lines in `v2-akis.cy.js`.

**Retraining invalidates `tests/parite.json`.** It records the model's sha256; `tests/parite.py` stops if they disagree. Always run `tests/parite.py --yaz` after `train.py` changes the model.

**Deployment state lives only in `web/site.json`.** Shadow / canary / progressive / rollback are all one number in that file, which is what makes every step a revertable commit (`RELEASE.md` §4). Tests control it with `cy.intercept`, so there is **no test backdoor in the app**.

## Git

This **is** a git repository: `main`, remote `origin` → <https://github.com/gonulnazire/primer>, pushed. (An earlier version of this file said otherwise; that is no longer true.)

The repo deliberately commits `cypress/videos/*.mp4` as delivery evidence, and `the_primer_v2_assignment.md` is deliberately gitignored.
