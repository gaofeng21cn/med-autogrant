# Fundability Strategy Prompt

Evaluate call fit, applicant evidence, innovation, feasibility, review risk, and funder-specific competitiveness.

Fundability is an AI-first MAG judgment. Schema completeness, OPL provider completion, queue state, package presence, or numeric scorecard values cannot create a fundability-ready verdict. When evidence is insufficient, return a typed blocker or owner receipt ref instead of a ready verdict.

Required outcome: `fundability_strategy_gate_recorded`, a verdict ref backed by grant-review evidence, or a typed blocker.
