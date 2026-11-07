# Decision and Action Accountability Kit

Use this record for actions that change an external system, communicate on behalf of an organisation, or are difficult to reverse. It keeps the proposal, permission, execution and observed result separate.

## 1. Action record

```yaml
action_id: "stable-action-id"
idempotency_key: "system:object:action:v1"
goal: "The outcome this action is intended to produce"
owner: "Named person accountable for the outcome"

proposal:
  proposed_by: "human | ai | service"
  proposed_action: "Exact intended action"
  assumptions:
    - "Assumption that must remain true"
  evidence:
    - "Test, observation, source or receipt supporting the proposal"

authorisation:
  authorised_by: "Named person or bounded policy"
  policy_version: "policy-name@version"
  authorised_scope: "What may be executed without a new decision"
  expires_at: "ISO-8601 timestamp or null for a durable policy"
  reauthorise_when:
    - "goal changes"
    - "action becomes difficult to reverse"
    - "external audience or target changes"
    - "supporting evidence is stale"

execution:
  status: "pending | inflight | succeeded | failed | unknown"
  executed_at: null
  executor: null
  exact_request: null
  external_receipt: null

observation:
  checked_at: null
  checked_by: null
  expected_signal: "What should become observable"
  actual_signal: null
  result: "pending | confirmed | contradicted | unavailable"

recovery:
  recovery_owner: "Named person"
  safe_retry_rule: "Retry only when no external result exists for the idempotency key"
  rollback_or_compensation: "Concrete recovery action"
  next_review_at: null
```

## 2. Decision rules

An autonomous worker may continue without another approval only when all of the following remain true:

- the goal is unchanged;
- the action stays inside the authorised scope;
- the action is reversible or has a tested compensation;
- current evidence still supports the decision;
- the responsible owner can inspect and correct the result.

Require a new human decision when any condition is false or cannot be verified.

## 3. Retry invariant

Never treat a timeout as proof of failure.

Before retrying an external action:

1. Search for a receipt using the same idempotency key.
2. Inspect the destination when a receipt is unavailable.
3. Retry only when the absence of the first action is confirmed.
4. Keep `unknown` as a distinct terminal state until reconciliation.

## 4. Review questions

- Can another person reconstruct the decision without private context?
- Does the record distinguish what was proposed from what was authorised?
- Is the exact external result visible rather than inferred from a local command?
- Is the recovery owner named?
- Would a delayed retry still operate under the correct policy and goal?

Source episode: [Why Can a System Be Smarter Than Its Leader? | Daniel Dennett](https://youtu.be/wuiq5XgRpgQ)
