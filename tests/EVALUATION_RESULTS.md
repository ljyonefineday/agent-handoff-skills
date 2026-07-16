# Protocol v2 evaluation results

Evaluation ran on 2026-07-16 against three fresh-context arms:

- **no-skill:** no handoff instructions;
- **current v1:** the three skills loaded from pinned commit `e7c2063`;
- **revised v2:** the working-tree skills, loading rare references only when their observable conditions occurred.

Each agent saw only the scenario content before `## Expected behavior`; the scoring agent alone saw the oracle and rubric. Seeded command results were treated as simulated fresh evidence and were not executed. One exploratory run per arm produced eight disposable artifacts. This report retains the scores and exact word counts without installing generated outputs as runtime assets.

## Weighted score

| Category | Weight | No-skill | Current v1 | Revised v2 |
|---|---:|---:|---:|---:|
| Continuity fidelity | 30 | 27 | 28 | 30 |
| Repository and secret safety | 20 | 20 | 18 | 20 |
| Validation honesty | 15 | 14 | 15 | 15 |
| Next-action executability | 15 | 9 | 13 | 15 |
| Resume correctness | 10 | 5 | 7 | 10 |
| Token economy | 10 | 8 | 4 | 10 |
| **Total** | **100** | **83** | **85** | **100** |

Revised v2 scored **100/100**, with **zero fatal errors** and no category regression against current v1.

## Create-plus-intake words

The count uses `[^\W_]+(?:[-'’][^\W_]+)*|\d+`, matching `tests/test_skills.py`.

| Scenario | No-skill | Current v1 | Revised v2 |
|---|---:|---:|---:|
| High-context dirty work | 488 | 875 | 447 |
| Small reconstructible task | 153 | 573 | 267 |
| Repository-only continuation | 392 | 675 | 343 |

Current v1 median: **675** words. Revised v2 median: **343** words. The median reduction is **49.2%**, exceeding the 30% acceptance threshold.

## Supplemental recovery check

After review tightened archival safety, a fresh revised-v2 agent ran both incompatible-init branches. The ordinary repair retained `validation_commands: []`. The owner-reported secret-bearing branch stopped before staging or archival, left every existing artifact unchanged, and created no repaired config. Result: PASS.

## Acceptance

- Revised score at least 90/100: PASS.
- No revised fatal error: PASS.
- No revised category regression: PASS.
- Median reduction at least 30%: PASS.

Result: **ACCEPT**.
