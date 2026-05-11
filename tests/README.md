# flowstate-api — unit tests

This directory contains the **unit test layer** for `flowstate-api`. Tests here cover
pure logic and model behaviour with no I/O, no HTTP client, and no running server.

For the full cross-repo test strategy and pyramid overview see
[`.docs/flowstate-mvp/TEST_STRATEGY.md`](../../.docs/flowstate-mvp/TEST_STRATEGY.md)
(created as part of TP-FLOWSTATE-000).

---

## Running the tests

```bash
# All unit tests with coverage (default)
pytest

# Unit tests only, skipping coverage overhead (fast local iteration)
pytest -m unit --no-cov

# Smoke subset only
pytest -m smoke
```

Coverage is configured in `pytest.ini` and fails under 95%. The sources measured are
`app/models`, `app/utils/auth`, `app/schemas`, `app/config`, and `app/database`.

---

## Test markers

Markers are declared in `pytest.ini`. Apply them with `@pytest.mark.<marker>`.

| Marker | When to use |
|---|---|
| `unit` | Every test in this directory — pure logic, no I/O |
| `smoke` | Minimal subset that must pass on every PR commit |
| `regression` | Full suite run; used in scheduled / merge jobs |
| `blocked_prd` | Test is written but the PRD behaviour isn't implemented yet |
| `current_behavior` | Asserts the current (non-PRD) behaviour as a tracked baseline |

Example:

```python
import pytest

@pytest.mark.unit
@pytest.mark.smoke
class TestPasswordPolicy:
    def test_minimum_length(self):
        ...
```

---

## Adding a test

1. Create a file under `tests/unit/` named `test_<module>.py`.
2. Mark every class or function with at least `@pytest.mark.unit`.
3. Add `@pytest.mark.smoke` to the single most critical case in each module so the
   PR fast-slice stays minimal.
4. Use `@pytest.mark.blocked_prd` when the corresponding `DM-FLOWSTATE-*` engineering
   ticket hasn't merged yet; remove the mark once it has.

No fixtures beyond what is in `tests/conftest.py` are needed for unit tests — if your
test requires a database session or HTTP client it belongs in a different layer (see
the strategy doc linked above).

---

## What is not here

| Layer | Location |
|---|---|
| White-box API integration (pytest + httpx ASGI) | [`pytest-api-framework/`](../../pytest-api-framework/) |
| Black-box API tests (Vitest + Ky + Zod) | `flowstate-api-tests-ts/` *(in progress)* |
| E2E journey tests (Playwright) | [`playwright-ts-framework/`](../../playwright-ts-framework/) |
