# Challenge 3: Evaluate answer quality

Time: ~30 minutes

## Objectives
- ✅ Complete a 10-row portal evaluation and find one quality improvement

## Context
Monitoring can show a fast, error-free answer that is wrong. A routine-monitoring recommendation for DRIVE-103 could have low latency and zero HTTP errors while missing its safety-sensitive compound failure. Evaluation compares answer quality with grounded expectations.

## Get started

1. In Foundry, open the project, then **Build** → **Evaluations** → **Create**.
2. Select **Agent** and choose `maintenance-efficiency-advisor-agent`.
3. Choose **Individual turns** and **Existing dataset**.
4. Name the dataset `industrial-asset-health-portal-10-cases` before uploading `labs/industrial-asset-health-portal/challenge-3-evaluate/eval_portal.jsonl`; upload remains disabled until a name is present.
5. Keep the `input` and `expected` field mapping unless the wizard asks you to set it.
6. Keep only quality evaluators needed for the lab, such as groundedness, relevance, coherence, and similarity. Uncheck tool-call accuracy because this advisor has no tool; checking it adds latency and produces an irrelevant poor score.
7. Submit and wait for all 10 rows to complete.
8. Record the aggregate scores from your run. Sort per-row results by lowest score, inspect evaluator rationale, and record one concrete instruction improvement. There is no predetermined expected score.

## Success criteria
- [ ] All 10 rows complete
- [ ] Aggregate and per-row scores are readable
- [ ] You identify one concrete improvement from a low-scoring case

Next: [Challenge 4 - Workflow](../challenge-4-workflow/README.md)