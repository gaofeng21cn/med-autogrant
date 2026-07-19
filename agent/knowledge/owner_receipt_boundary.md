# Owner Receipt Boundary Knowledge

## Purpose

This knowledge boundary defines what MAG owner receipts prove during Codex-first grant stages.

## What Receipts Can Prove

- A MAG-owned stage action, blocker, handoff, no-regression result, memory decision, lifecycle ref, safe action, or package ref was accepted by the domain authority boundary.
- The output has an owner, source refs, provenance, timestamp/runtime evidence ref, and next-stage effect.
- A typed blocker is legitimate only for a real hard boundary; ordinary quality gaps use diagnostics and route recommendations.

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
- OPL Stage Review receipts bind the context-isolated identity of each reviewed scope and its reviewed artifacts, rubric, and verdict; unrelated package hashes do not widen that binding, and the receipts do not sign MAG readiness authority.
- MAG package receipts sign package/export state and manual portal boundary only after consuming current dependency-scoped review evidence, the identity-bound Stage Review receipt, and separate exact-byte release-integrity evidence.

## Blocker Expectations

If a receipt is missing, malformed, body-bearing, or mechanically claims readiness, reject the ready claim, record quality debt, and proceed with a diagnostic. Use a typed blocker only when the defect creates wrong-target, authority, safety, irreversible-action, unavailable-executor, or explicit human-decision risk.

## Review Questions

- What exactly did MAG accept: handoff, blocker, package ref, memory decision, or verdict ref?
- Which next-stage action is authorized, and which readiness claims remain open?
