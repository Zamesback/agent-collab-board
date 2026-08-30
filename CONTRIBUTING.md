# Version Management & Collaboration Guidelines

This document defines the version management approach for AgentNexus. All collaborators (humans + AI agents) must comply.

## Version Numbers (SemVer)

- Format: `MAJOR.MINOR.PATCH` (e.g., `v2.1.0`)
- Current baseline: **v2.0.0**
- Incremental features / new requirements → MINOR +1 (`2.1.0`, `2.2.0`...)
- Compatibility fixes → PATCH +1
- Breaking changes / major redesign → MAJOR +1 (`3.0.0`)
- Each version gets corresponding tag on `main`

## Branch Strategy

- **`main`**: Stable mainline, always runnable, only accepts verified merges
- Each new requirement: branch `feature/<brief-description>` from `main` (e.g., `feature/template-engine`)
- After completion + verification passed: merge back to `main`, delete feature branch
- Use lowercase hyphens for naming, concise and meaningful

## Commit Convention (Conventional Commits)

Format: `<type>(<scope>): <description>`

| type | Purpose |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `refactor` | Refactoring (no behavior change) |
| `test` | Testing related |
| `chore` | Build/tools/miscellaneous |

Example: `feat(api): support Tongyi Qianwen compatible interface`

## Release Process

1. Requirement confirmation → branch `feature/xxx` from `main`
2. Development implementation → verify against task acceptance criteria
3. Update `CHANGELOG.md` (new version entry)
4. Merge to `main` → tag `vX.Y.Z` → push (`main` + tag)

## Task Assignment Guidelines

- After each requirement is broken into tasks, in addition to marking priority, **must simultaneously assign owner (assignee)**, visible on the board
- Assignment principle: Planner Agent and Executor Agent each claim a portion, avoid single-point backlog
- Unimplemented tasks **must not be marked done**; tasks marked done must have verifiable implementation in code

## Security Guidelines

- `project_config.json` (including api_key encrypted storage), `*.lock`, `*.tmp`, `api_calls.log` are in `.gitignore`, **forbidden** to commit
- Remote uses **SSH** (`git@github.com:Zamesback/agent-nexus.git`), **forbidden** to embed token in URL
- Plaintext keys forbidden in code

## Collaboration Data Files

- `collab_board.json`: Multi-agent collaboration board data (tasks/messages/agents), is the single source of truth for collaboration
- **Only incremental modifications** (append messages, update task fields), **never overwrite the entire file**
