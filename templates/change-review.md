# Invariant-aware change review

## Change

- What is changing?
- Which component owns the decision?
- What is explicitly out of scope?

## Preserved properties

- Which invariants apply?
- What observable state would violate each one?
- Which automated check detects that state?

## Boundary cases

- concurrent requests;
- retries and duplicate delivery;
- partial failure;
- stale authorization;
- migration and rollback;
- time-zone and interval boundaries.

## Evidence

- exact test or monitor result;
- version or commit tested;
- unresolved limitation;
- person or component responsible for follow-up.
