# AGENTS.md

Repo containing agent-facing skills (open skills format). Humans are welcome;
agents, read this first.

## What lives here

`skills/<skill-name>/` — each folder is one self-contained skill:

- `SKILL.md` — the skill. YAML frontmatter (`name`, `description`) + workflow
  body. The description is the trigger surface: write it pushy and concrete,
  it decides when agents engage.
- `references/` — runbooks loaded only when the relevant path is taken
  (per-platform documentation lives here, not in SKILL.md).
- `scripts/` — executable helpers. Deterministic shells of the runbook; keep
  them single-purpose and testable via CLI flags.

## Conventions

- Skills must be agent-agnostic: no tool paths or harness names that only one
  agent understands; plain CLI commands and file paths.
- Runbooks state their machine-verification status in a header note with a
  date. Update it when you actually verify a platform.
- Toolchain policy for any new skill: detect-and-use what exists; never
  auto-install multi-gigabyte platform SDKs; stop with the exact remediation
  command when a dependency is missing.
- Screenshots produced by these skills are real captures — never rendered
  mockups. Demo state injection at runtime is allowed but must be disclosed.
