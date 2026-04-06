# Project Instructions

This file contains instructions for Claude when working in this project.

## Overview

Describe your project here — its purpose, tech stack, and key architectural decisions.

## Development Guidelines

- Follow the rules defined in `.claude/rules/`
- Use the skills defined in `.claude/skills/` for specialized tasks
- Use the commands defined in `.claude/commands/` for common workflows

## Key Conventions

- **Testing**: See `.claude/rules/testing.md`
- **API Design**: See `.claude/rules/api-design.md`

## Project Structure

```
.
├── CLAUDE.md              # This file
├── .mcp.json              # MCP server configuration
├── .worktreeinclude       # Files included in git worktrees
└── .claude/
    ├── settings.json      # Shared Claude Code settings
    ├── settings.local.json# Local overrides (not committed)
    ├── rules/             # Rule files loaded as context
    ├── skills/            # Reusable skill definitions
    ├── commands/          # Custom slash commands
    ├── output-styles/     # Output formatting styles
    ├── agents/            # Sub-agent definitions
    └── agent-memory/      # Persistent agent memory
```
