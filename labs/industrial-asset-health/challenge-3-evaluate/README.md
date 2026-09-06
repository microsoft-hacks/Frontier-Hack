# Challenge 3: Evaluate answer quality

Time: ~30 minutes

## Objectives
- ✅ Run a 10-case quality evaluation and identify one concrete improvement

## Context
Monitoring can show a fast, error-free response that is still wrong. For example, advising routine monitoring for DRIVE-103 in 300 ms would look operationally healthy while missing a safety-sensitive compound failure. Evaluation measures correctness against expected outcomes.

## Get started

1. In Foundry, open the project, then **Build** → **Evaluations** → **Create**.
2. Select **Agent** as the target and choose `maintenance-efficiency-advisor-agent`.
3. Choose **Individual turns** and **Existing dataset**.
4. Name the dataset `industrial-asset-health-10-cases` first, then upload `challenge-3-evaluate/eval_portal.jsonl`. Upload remains disabled until the dataset has a name.
5. Keep the default mapping of `input` to input and `expected` to expected result unless the wizard requests explicit mapping.
6. Keep only relevant quality evaluators such as groundedness, relevance, coherence, and similarity. Uncheck tool-call accuracy: this target has no tool and local function tools cannot execute in this evaluation path, so that evaluator adds latency and misleadingly poor scores.
7. Submit and wait until all 10 rows finish.
8. Record the aggregate scores produced by your run. Sort rows by lowest score, read their input, expected result, output, and evaluator rationale, then write down one specific instruction improvement. Do not assume a target score.

## Success criteria
- [ ] All 10 rows complete
- [ ] Aggregate and per-row scores are readable
- [ ] You identify one concrete improvement from the lowest-scoring row

Next: [Challenge 4 - Workflow](../challenge-4-workflow/README.md)