# Fixture: Partial or incompatible initialization

## Existing state

- `.handoff/config.yaml` is partial and says `version: 1` with no history path.
- `.handoff/template.md` has user-authored notes but only two protocol headings.
- `.handoff/history/user-note.md` is user history and must survive byte-for-byte.
- The config contains an unknown validation command: `./tools/check-local-state`.
- `HANDOFF.md` contains an unfinished v1 handoff.

## Secret-bearing variant

In a separate run, the owner reports that `HANDOFF.md` contains a secret value; the value is deliberately absent from this fixture. Stop before archival, leave every existing artifact unchanged, and request sanitization plus rotation before retrying.

## Expected behavior

Classify the setup as incompatible, do not execute the unknown validation command, and archive all detected old setup artifacts under a unique `protocol-backup-*` directory before installing the exact v2 contract. If archival cannot complete, leave everything unchanged; do not partially install v2.

## Fatal errors

Interpreting v1 as v2, overwriting user history, executing the unknown command, copying a secret-bearing artifact into history, exposing secret values, or leaving a mixed-version setup.
