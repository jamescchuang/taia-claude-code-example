# Security Review Skill

Performs a structured security review of code changes.

## Usage

Invoke this skill when you need to audit code for security vulnerabilities before merging or deploying.

## What This Skill Does

1. Reads the diff or specified files
2. Checks against the security checklist in `checklist.md`
3. Reports findings grouped by severity: Critical, High, Medium, Low, Info
4. Suggests remediations for each finding

## Trigger

Use this skill by saying:
- "Run a security review on these changes"
- "Security review the files in `src/auth/`"
- `/security-review`

## Output Format

```
## Security Review

### Critical
- [ ] Finding description (file:line)

### High
- [ ] Finding description (file:line)

### Findings Summary
X critical, X high, X medium, X low
```
