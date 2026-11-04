from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED = {
    "id",
    "statement",
    "owner",
    "scope",
    "violation",
    "check",
    "evidence",
    "review_on",
}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_document(document: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["document must be an object"]

    if not isinstance(document.get("system"), str) or not document["system"].strip():
        errors.append("system must be a non-empty string")

    invariants = document.get("invariants")
    if not isinstance(invariants, list) or not invariants:
        errors.append("invariants must be a non-empty array")
        return errors

    seen: set[str] = set()
    for index, invariant in enumerate(invariants):
        prefix = f"invariants[{index}]"
        if not isinstance(invariant, dict):
            errors.append(f"{prefix} must be an object")
            continue

        missing = REQUIRED - invariant.keys()
        if missing:
            errors.append(f"{prefix} missing: {', '.join(sorted(missing))}")
            continue

        invariant_id = invariant["id"]
        if not isinstance(invariant_id, str) or not ID_PATTERN.fullmatch(invariant_id):
            errors.append(f"{prefix}.id must be lowercase kebab-case")
        elif invariant_id in seen:
            errors.append(f"{prefix}.id duplicates {invariant_id}")
        else:
            seen.add(invariant_id)

        for field in ("statement", "owner", "scope", "violation", "evidence"):
            if not isinstance(invariant[field], str) or not invariant[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

        check = invariant["check"]
        if not isinstance(check, dict):
            errors.append(f"{prefix}.check must be an object")
        else:
            for field in ("type", "command"):
                if not isinstance(check.get(field), str) or not check[field].strip():
                    errors.append(f"{prefix}.check.{field} must be a non-empty string")

        review_on = invariant["review_on"]
        if not isinstance(review_on, list) or not review_on:
            errors.append(f"{prefix}.review_on must be a non-empty array")
        elif any(not isinstance(item, str) or not item.strip() for item in review_on):
            errors.append(f"{prefix}.review_on entries must be non-empty strings")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_invariants.py PATH", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{path}: {exc}", file=sys.stderr)
        return 2

    errors = validate_document(document)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"{path}: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
