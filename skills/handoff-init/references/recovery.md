# Handoff Init Recovery

Use this reference only after observing partial or damaged files, a non-v2 contract, or an unsafe configured path. Non-v2 setup is incompatible; never merge or reinterpret it as v2.

## Inspect without mutation

Inventory existing config, template, active artifact, extra setup files, and user history. Capture enough names and content hashes to verify preservation. Do not execute an unknown validation command. Reject absolute paths, `..` traversal, and symlink resolution outside the repository; record an unsafe path string without following it.

## Archive before installing v2

Before copying, assess each candidate without printing sensitive content. If any candidate is known or suspected to contain a secret value, stop before copying or archival. Leave all existing setup unchanged and ask the owner to sanitize the artifact and rotate any exposed secret; resume migration only after the risk is cleared.

1. Choose a unique staging directory inside the repository. Its final name must begin `.handoff/history/protocol-backup-` with a UTC timestamp and a unique suffix when that name already exists.
2. Archive all detected existing old setup artifacts outside the history directory: config, template, any safely resolved active artifact, and other protocol files. Keep existing user history byte-for-byte in place. Include an inventory so unsafe or unavailable artifacts remain explicit.
3. Verify every archived copy before moving or replacing any original. Rename the completed staging directory to its final backup name atomically.
4. Only after the archive is complete may you remove archived old contract files and install the exact v2 config and template. Do not fabricate an active handoff.

If archival fails, leave everything unchanged: remove only newly created staging data, do not move or rewrite any existing artifact, and report the failure. If cleanup cannot be confirmed, stop and report that residue without touching originals.

## Repair cases

- Partial or damaged setup: treat the whole detected contract as incompatible and use the archive-first sequence.
- Unknown validation command: preserve it only in the verified backup; do not carry it into the repaired v2 config, which must use `validation_commands: []`. The owner may add it later after proving it is safe validation.
- Unsafe active or history path: never read, copy, create, or delete outside the repository root. Use the canonical v2 paths only after the safe artifacts are archived.
- Backup-name collision: add a new suffix; never overwrite or prune history.

Finish by verifying exact v2 files, unchanged user history, absence of a fabricated active artifact, and the final backup inventory.
