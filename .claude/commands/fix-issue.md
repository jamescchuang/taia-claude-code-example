# Fix Issue Command

Slash command: `/fix-issue`

## Usage

```
/fix-issue <issue-number>
/fix-issue <issue-url>
/fix-issue <description>
```

## What This Command Does

1. **Fetch the issue** — reads the issue title, description, and comments
2. **Reproduce the problem** — identifies the relevant code and understands the root cause
3. **Implement a fix** — makes the minimal change necessary to resolve the issue
4. **Write a test** — adds or updates a test that would have caught this bug
5. **Summarize** — explains what was changed and why

## Guidelines

- Fix the root cause, not just the symptom
- Do not refactor unrelated code while fixing the issue
- Keep the diff small and focused
- Reference the issue number in the commit message: `fix: resolve NPE in user loader (closes #123)`

## Example

```
/fix-issue 42
```

Claude will fetch issue #42, diagnose the problem, apply a targeted fix, and verify it with a test.
