# MAG Authority Functions

Owner: `Med Auto Grant`
Purpose: `minimal_authority_function_catalog`
State: `declaration_surface`
Machine boundary: This directory declares MAG-owned authority functions for OPL stage-pack consumption. It is not a generic runner, scheduler, queue, attempt ledger, runtime state root, or artifact body store.

MAG retains authority for owner receipts, typed blockers, grant quality/export verdicts, package authority, and grant strategy memory accept/reject decisions. OPL generated surfaces may consume body-free refs and receipts; they must not write grant truth, artifact bodies, owner receipt bodies, typed blocker bodies, runtime state, queues, caches, or generated artifacts from this declaration.
