# Grant Meta Review Policy

## Entry Conditions

- A reviewable draft, accepted aims, call criteria, and claim/source ledger exist.
- Known fundability risks and authoring constraints are visible to the reviewer.
- Quality verdict is still open and must be decided by AI-first review evidence.

## Stage Work

- Run a context-isolated whole-grant critique in a new StageRun/Attempt and map each defect to its earliest owning Stage.
- Produce or update issue matrix, closure dossier, quality-diff refs, and residual risk refs.
- Return route-back and closure criteria; do not mutate proposal artifacts inside this Stage.

## Exit Conditions

- `grant_review_gate_receipt_recorded` exists with quality verdict refs backed by critique/closure evidence; or
- A `route_back_ref` records an ordinary critique, claim/source, major-issue, or rebuttal repair target; or
- A quality-debt diagnostic records semantic-evidence gaps and may recommend route-back; a typed blocker is reserved for a real authority, safety, identity, irreversible-action, executor, or human-decision boundary; or
- A MAG owner receipt signs quality gate state.

## Handoff

- Handoff target: `package_and_submit_ready`.
- Handoff must include critique refs, issue closure state, quality verdict ref or blocker, residual risk, package-facing requirements, and reviewer independence evidence.
- Material unclosed issues block package readiness.

## Independent Review And Gate Expectation

- Independent review is mandatory for quality readiness unless a receipt explains an equivalent reviewer artifact.
- The meta reviewer cannot inherit or resume an author, repairer, or prior reviewer thread; same-thread refinement is not Review.
- Required gates: `quality`, `fundability`, and `authority_boundaries`.
- Scorecards and quality-diff reports organize evidence; they do not independently decide ready.

## OPL Role Boundary

- OPL role: descriptor, receipt, and operator projection consumer.
- OPL cannot produce AI-free quality verdicts or mutate grant truth.
- Allowed action refs: `open_grant_user_loop`, `inspect_progress`.

## Non-Pass Signals

- The critique has no severity, closure criterion, or post-revision evidence.
- Quality readiness depends on scorecard completion instead of independent review.
