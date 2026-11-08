# What the research says about debate and judging

The rules in `SKILL.md` follow from these results. Each row keeps the study's limit, because most were measured on benchmark questions with one right answer, not on open design choices made by frontier coding agents. Links and access dates are in [sources.md](sources.md).

## Debate

| Result | Study | What it means here |
| --- | --- | --- |
| Multi-round debate improved factuality and reasoning on the tasks studied | Du et al., 2023 (ICML 2024) | Debate can help, but the study does not show it beats an equal budget spent elsewhere |
| Debate counters a single model's inability to generate new ideas once it is confident | Liang et al., EMNLP 2024 | Distinct lenses are the point; one model restating itself adds little |
| Debate did not reliably beat self-consistency without tuning | Smit et al., 2023 | Compare against independent sampling before paying for rounds |
| Majority voting explains most of the gains attributed to debate across seven benchmarks | Choi, Zhu, and Li, NeurIPS 2025 | For a checkable answer, collect independent answers; seek new evidence rather than more persuasion |
| Accuracy fell over rounds as models flipped correct answers to agree, even when stronger models outnumbered weaker ones | Wynn, Satija, and Hadfield, 2025 | Positions change only on evidence; save first positions; check for correct-to-wrong flips |
| Agents reinforce peers instead of evaluating them | Pitre, Ramakrishnan, and Wang, ACL Findings 2025 | Permit disagreement explicitly and measure changed answers |
| Homogeneous debate used 2.1 to 3.4 times the tokens of isolated self-correction for equal or lower accuracy (ten-agent teams of small open models) | Bertalanič and Fortuna, 2026 | Keep isolated baselines; diversity of model and lens, not head count, is what debate buys |
| Additional discussion rounds could reduce performance; the best decision protocol depended on the task | Kaesberg et al., ACL Findings 2025 | Unanimity is not automatically the right stop condition; cap rounds |
| Debate raised a non-expert judge's accuracy from 48% to 76% (model judges) and from 60% to 88% (human judges) | Khan et al., 2024 | The use that transfers: debate informs an adjudicator who checks the evidence |
| Self-correction without external feedback sometimes degraded performance | Huang et al., ICLR 2024 | Revision rounds work when they bring executed tests, validators, or sources |

## Judging

| Result | Study | Control in `SKILL.md` |
| --- | --- | --- |
| LLM judges show position, verbosity, and self-enhancement biases, while agreeing with humans about as often as humans agree with each other | Zheng et al., NeurIPS 2023 | Swap order; penalize length that adds nothing; judges inform, checks decide |
| Evaluators recognize and favor their own generations, and the bias grows with self-recognition | Panickssery, Bowman, and Feng, NeurIPS 2024 | Judge from a different model family; blind labels, knowing that style can still reveal the author |
| Judges prefer text with lower perplexity to them, regardless of who wrote it | Wataoka et al., 2024 | Same-family judging is biased even without labels |
| A panel of smaller, diverse judges beat a single large judge, with less bias and lower cost | Verga et al., 2024 | For taste or design questions, a diverse panel; for checkable criteria, one judge plus executed checks |
| Responses that match the listener's view are preferred, sometimes over correct ones | Sharma et al., 2023 (revised 2025) | In a debate the listener is the coordinator or the other agent; agreement is never the success condition |
| Most multi-agent failures trace to system design: vague specifications, misalignment between agents, and missing verification | Cemri et al., NeurIPS 2025 | Fixed frame, stable finding IDs, explicit stop rules, and verification outside the debate |

## Lessons from a four-round review

A real design review between two model families, recorded on disk, reached full agreement after four rounds. Findings fell from 13 (2 blockers, 9 shoulds, 2 nits) to 4, then 3, then 0. What it teaches:

- **What worked.** Independent drafts from two families and two lenses surfaced five real conflicts a single draft would have hidden. A fresh evaluator context each round, stable IDs, a three-level severity, and an explicit verdict line made closure trackable. The coordinator verified each decisive claim at the source before accepting it, and twice accepted the substance while refining the wording, with reasons the evaluator then accepted.
- **What failed.** No round cap or budget was declared, so agreement was the only stop rule. The coordinator accepted about 18 findings and rejected none outright, so the evaluator became the de facto author. The artifact grew 78% across rounds while the user's top priority was brevity. Evaluator reports were condensed in place, so the raw evidence could not be re-audited. Requirements changed twice mid-round, which a scope check before the first costly round would have caught.
- **What the skill changes.** A budget and a per-finding round limit before dispatch; raw reports saved separately from summaries; rejection as a normal, logged outcome; the acceptance rate and net size reported each round; a scope and authorization check before costly rounds, asking the user only about an unresolved decision.

Fewer objections and a final agreement do not show that the result improved outcomes. That needs a behavioral check, such as running the resulting skill with and without it.
