# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Lab 3 of the TAIA Claude Code course — demonstrates Claude Code **sub-agents** ("一人公司、不同角色 AI 代理人"). Content is teaching material, not production code (see `README.md` disclaimer).

## Running the Demo

`index.html` is a standalone static page — no build step, no dependencies.

```bash
open index.html
```

It fetches live weather from Open-Meteo (`https://api.open-meteo.com/v1/forecast`) for Taipei (25.0330, 121.5654) on page load. Opening via `file://` is fine; the API supports CORS. There is no test suite, linter, or package manager in this lab.

## Sub-Agent Architecture

Sub-agents live under `.claude/agents/<name>.md` and are auto-discovered by Claude Code. Each agent definition uses frontmatter (`name`, `description`, `model`, `color`, `memory`) followed by the agent's system prompt. `description` drives when the parent routes work to the sub-agent — keep it specific (e.g. the existing `marketing-content-creator` uses `"use this agent after you are done writing code"`).

When `memory: project` is set in frontmatter, the agent also gets a persistent, file-based memory store at `.claude/agent-memory/<agent-name>/`, organized as:

- `MEMORY.md` — index of one-line pointers (always loaded into the agent's context; keep under ~200 lines)
- Individual memory files with frontmatter (`name`, `description`, `type`) where `type` ∈ `user | feedback | project | reference`

This memory is project-scoped and versioned with the repo, so it's shared with the team. Don't store ephemeral task state, code patterns derivable from the repo, or secrets here — see the in-file guidance at the bottom of `marketing-content-creator.md` for the full rules.

## Adding a New Sub-Agent

1. Create `.claude/agents/<name>.md` with frontmatter + system prompt.
2. If the agent should have persistent memory, add `memory: project` and create `.claude/agent-memory/<name>/` (Claude will write into it on first save).
3. Write the `description` from the parent's perspective — it's what Claude reads to decide whether to delegate.

## Running a Sub-Agent

當程式已完成，檢查是否有接續執行的 sub agent