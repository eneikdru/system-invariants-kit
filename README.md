# System Invariants Kit

A small, executable way to describe what a system must preserve before an
engineer or an AI agent changes it.

The kit keeps three things together:

1. the invariant;
2. an observable violation;
3. the check that should detect that violation.

This is intentionally narrower than an architecture framework. It is a review
artifact that can live beside code and fail CI when its structure degrades.

## Quick start

```powershell
python tools/validate_invariants.py examples/booking/invariants.json
python -m unittest discover -s tests -v
```

## Example

```json
{
  "id": "no-double-booking",
  "statement": "One resource cannot have overlapping confirmed bookings.",
  "owner": "booking-service",
  "scope": "confirmed bookings for the same resource",
  "violation": "Two overlapping confirmed intervals exist for one resource.",
  "check": {
    "type": "concurrency-test",
    "command": "python -m unittest tests.test_booking_concurrency"
  },
  "evidence": "CI test result",
  "review_on": ["schema-change", "storage-change", "booking-write-change"]
}
```

## Repository structure

- `schema/invariant.schema.json`: machine-readable contract.
- `examples/booking/invariants.json`: concrete example.
- `templates/invariant.json`: copyable starting point.
- `templates/change-review.md`: review checklist.
- `tools/validate_invariants.py`: dependency-free structural validator.
- `tests/`: validator regression tests.

## Working rule

An invariant is incomplete when it only says what should happen. It must also
say what failure looks like and how that failure will be detected.

## License

MIT
