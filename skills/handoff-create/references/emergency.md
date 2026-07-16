# Handoff Create Emergency Cases

Load this reference only after observing missing or incompatible setup, or a collision while archiving the active artifact.

## Missing or incompatible setup

Do not invent a fallback artifact. If config or template is absent, invoke the repository's handoff initialization workflow, then re-read both files and continue only after exact v2 setup is verified. If setup is non-v2, stop creation and let initialization archive and replace it; creation never interprets or migrates old protocol content. If initialization is unavailable or fails, report the blocker and leave the worktree unchanged.

Never follow an absolute or escaping configured path, and never carry an unknown validation command forward as trusted evidence.

## Archive collision or failure

Before replacing an active artifact, copy it into the configured history directory using its handoff ID or timestamp. Verify that source and destination both remain inside the repository root.

If the active artifact is known or suspected to contain a secret value, stop before copying or archival. Keep the active artifact and all existing work unchanged, and ask the owner to sanitize it and rotate any exposed secret before retrying.

If the destination exists, add a unique suffix and retry with a new name; never overwrite, prune, or reuse an archive. Verify the archived copy before replacing the active artifact. If any archive step fails, keep the old active artifact and all implementation files unchanged, do not write the replacement, and report the exact failure.

The mutation allowance remains limited to the new archive and active handoff. Do not reset, clean, stash, switch branches, discard work, alter the index, or create a checkpoint without explicit authorization.
