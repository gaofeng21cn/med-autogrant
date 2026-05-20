# Owner Receipt Boundary Knowledge

## Purpose

This knowledge boundary defines what MAG owner receipts prove during Codex-first grant stages.

## What Receipts Can Prove

- A MAG-owned stage action, blocker, handoff, no-regression result, memory decision, lifecycle ref, safe action, or package ref was accepted by the domain authority boundary.
- The output has an owner, source refs, provenance, timestamp/runtime evidence ref, and next-stage effect.
- A typed blocker is legitimate and should stop or redirect a stage.

## What Receipts Cannot Prove

- They cannot store grant truth bodies, proposal text, private evidence, memory bodies, or verdict bodies in repo source.
- They cannot turn runtime queue state, provider completion, schema completeness, scorecard values, or package existence into readiness.
- They cannot let OPL claim MAG fundability, quality, or export authority.

## Required Receipt Fields

- Owner: `med-autogrant`.
- Action or blocker kind.
- Source refs and provenance refs.
- Authority surface or stage id.
- Allowed next-stage effect: proceed, repair, stop, terminal package handoff, or evidence request.
- Body-free artifact, memory, verdict, or package refs when relevant.

## Stage Use

- Intake receipts sign source sufficiency or blocker state.
- Fundability receipts sign proceed/repair/retarget/stop state.
- Aims receipts sign route/structure acceptance.
- Authoring receipts sign draft/ref acceptance, not quality readiness.
- Review receipts sign quality gate state.
- Package receipts sign package/export state and manual portal boundary.

## Blocker Expectations

If a receipt is missing, malformed, body-bearing, or mechanically claims readiness, the stage must return a typed blocker rather than proceed.

## Review Questions

- What exactly did MAG accept: handoff, blocker, package ref, memory decision, or verdict ref?
- Which next-stage action is authorized, and which readiness claims remain open?
