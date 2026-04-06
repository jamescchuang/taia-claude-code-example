# Testing Rules

Rules and conventions for writing tests in this project.

## General Principles

- Write tests that verify behavior, not implementation details
- Each test should have a single, clear assertion focus
- Test names should describe the scenario and expected outcome

## Test Structure

- Unit tests live alongside source files as `*.test.ts` / `*.spec.ts`
- Integration tests live in a top-level `tests/integration/` directory
- Use descriptive `describe` and `it` blocks

## What to Test

- All public API surfaces
- Edge cases and error paths
- Business-critical logic

## What NOT to Do

- Do not mock the database in integration tests
- Do not test framework internals
- Do not write tests that depend on execution order
