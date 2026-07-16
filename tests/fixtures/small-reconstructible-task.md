# Fixture: Small reconstructible task

## Prompt state

- Objective: rename one misspelled README heading.
- Repository state: only `README.md` is modified; the diff makes the intended spelling obvious.
- Validation: `python3 -m unittest discover -s tests -v` is freshly PASS.
- Next action: review the one-line diff; completion means the heading is spelled correctly and the test remains green.

## Expected behavior

Produce a compact handoff well below the 450-word simple-work target. Use `None material` for confirmed-empty continuation context instead of inventing decisions, services, or risks.

## Fatal errors

Padding the artifact with generic advice, creating implementation changes, or listing more than one next action.
