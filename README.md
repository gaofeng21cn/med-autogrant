<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**A medical grant-authoring mainline for investigator-side `NSFC`-style applications**

> `Med Auto Grant` is the medical grant line in the broader `Grant Foundry` family. It is built to help applicants turn background, prior work, preliminary evidence, and topic ideas into a governed authoring and revision process instead of a pile of disconnected drafts.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Medical researchers, clinical teams, faculty members, and PIs preparing investigator-side grant applications
    </td>
    <td width="33%" valign="top">
      <strong>What It Helps With</strong><br/>
      Question refinement, applicant-fit checking, structured drafting, mentor-style critique, revision, and local submission packaging
    </td>
    <td width="33%" valign="top">
      <strong>Public Role</strong><br/>
      The active medical `Grant Ops` repository line, with top-level federation admission and handoff wording still separately gated at `OPL`
    </td>
  </tr>
</table>

## What It Helps With

- Turn applicant materials, prior work, ongoing projects, and preliminary evidence into a clearer `NSFC`-style grant line.
- Keep question refinement, argument building, drafting, critique, and revision on one governed author-side path.
- Preserve revision evidence and verdict checkpoints instead of losing them across scattered documents and chat history.
- Export a local `submission-ready` package once the workspace is frozen and evidence-complete.

## Current Public Path

| Path | Status | What it means |
| --- | --- | --- |
| Structured grant authoring mainline | Active | The current honest path from topic refinement to draft and freeze |
| Mentor-style critique and revision evidence | Active | Review, revision, and re-review evidence stay on the same author-side line |
| Local `submission-ready` package export | Active local output | Landed for frozen, evidence-complete workspaces; this is still not external website submission |
| Mature hosted runtime or external-submission autopilot | Not landed | Still future work |

## Best-Fit Use Cases

- You are preparing an investigator-side medical grant application with reusable author materials.
- You need stronger question refinement before committing to full drafting.
- You want critique and revision to stay structured and auditable rather than informal.
- You want a local package that is closer to submission readiness before final human review.

## How To Read This Repository

1. Potential users should start here, then continue to the [Docs Guide](./docs/README.md), [Domain Positioning](./docs/domain-positioning.md), and [MVP Scope](./docs/mvp-scope.md).
2. Technical readers and planners should read [Project](./docs/project.md), [Status](./docs/status.md), [Architecture](./docs/architecture.md), [Invariants](./docs/invariants.md), [Decisions](./docs/decisions.md), and [Contracts Overview](./contracts/README.md).
3. Developers and maintainers should continue into `docs/specs/`, `docs/references/`, `docs/plans/`, and `docs/history/omx/`.

## Plain-Language Boundary

`Med Auto Grant` is not the whole top-level federation and it is not the external submission website.
Its job is to own grant-domain truth on the applicant side.

```text
User / Agent
  -> OPL Gateway (optional)
      -> Med Auto Grant
          -> Runtime Substrate
              -> Grant-Domain Truth
```

In plain language:

- `OPL` stays above this repository and governs family-level admission and handoff wording.
- `Med Auto Grant` owns the grant authoring workflow, revision logic, and grant-domain truth.
- The runtime substrate should not be confused with the public product surface.

## What This Repository Is Not

- It is not a claim that a mature hosted grant frontend has landed.
- It is not a claim that the system will automatically submit to external funding websites for you.
- It is not a reason to blur `OPL`, runtime substrate, and applicant-side grant truth into one layer.

<details>
  <summary><strong>Technical Notes And Current Runtime Truth</strong></summary>

The current executable mainline is `CLI-first + real upstream Hermes-Agent runtime substrate`.
The repo-tracked truth set also keeps the phrase real upstream `Hermes-Agent` runtime substrate explicit for this mainline.
The repo-tracked current-program pointer remains `contracts/runtime-program/current-program.json`.
Machine-local runtime state remains under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.
Legacy repo-local runtime helpers now survive only as a compatibility bridge and regression oracle rather than the substrate owner.
Repo-local adapters such as `hermes_runtime.py` and `domain_entry.py` preserve domain semantics, but they are not the runtime substrate owner.

The current formal-entry matrix remains `CLI`, `MCP`, and `controller`.
The repository mainline remains `Auto-only`.

The lightweight structured `product entry` shell is now landed.
That shell is already schema-backed where the contract surfaces have been frozen, and it also feeds the hosted contract bundle, hosted caller, and external caller handoff path through `domain_entry_contract`, `schema_contract`, `authoring_contract`, `supported_commands`, and `command_contracts`.
These repo-tracked surfaces still do not mean an actual hosted runtime has landed, and a richer grant-facing product experience still remains future work.
The current ideal target keeps `OPL` above the domain line while the grant surface stays applicant-side and machine-readable.

The current landed product-facing surfaces now include:

- `MedAutoGrantDomainEntry` as the service-safe domain entry contract
- `product build-entry`, `product preflight`, `product start`, `product manifest`, and `product frontdesk`
- `workspace progress`, `workspace cockpit`, `product direct-entry`, and `product user-loop`
- `package submission-ready` for local fail-closed submission packaging
- `hosted contract bundle` output for hosted caller / external caller consumption
- `domain_entry_contract`, `schema_contract`, `authoring_contract`, `supported_commands`, and `command_contracts` as the machine-readable handoff catalog

These surfaces make the grant line more navigable and machine-readable, but they do not mean a mature hosted product frontend or external-submission autopilot has landed.
</details>

## Development Verification

- `make test-fast`
- `make test-meta`
- `make test-cli-smoke`
- `make test-full`

## Further Reading

- [Docs Guide](./docs/README.md)
- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)
- [Project](./docs/project.md)
- [Status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Contracts Overview](./contracts/README.md)
