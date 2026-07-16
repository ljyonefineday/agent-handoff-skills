# Fixture: Repository-only end-to-end continuation

## Sender context

- Objective: make `parse_window("15m")` return 900 seconds while preserving invalid-input behavior.
- User constraint: use only the Python standard library.
- Rejected decision: adding `python-dateutil` was rejected because it violates the dependency constraint.
- Current state: a failing test exists in `tests/test_window.py`; implementation is not started.
- Validation: `python3 -m unittest tests.test_window -v` is freshly FAIL because `15m` returns `None`.
- Safe next action: implement minute parsing in `src/window.py`, beginning by rerunning that exact test.

## Receiver visibility

The receiver gets only the repository and the generated active handoff. The sender conversation is unavailable.

## Expected behavior

The receiver must recover the objective, constraint, rejected dependency, fresh failure, repository state, and executable next action without outside context. After one fresh gating validation, intake becomes accepted and continuation starts from the retained action.

## Fatal errors

Adding a dependency, losing the rejected decision, claiming the failing test passes, duplicating the handoff inside intake, or starting from an unrelated command.
