# CLAUDE.md

## Purpose

This repository is used to demonstrate a realistic Claude Code workflow on top of an existing production-style codebase.

The agent working in this directory and GitHub repository `full-stack-fastapi-template` is tasked with solving GitHub issues or feature requests, not generating disconnected demo code. Work should begin from a stated requirement, issue description, or acceptance criteria and should end with validated changes and a PR-ready summary.

## Primary Goal

When operating in this repository, the agent should:

1. Read and interpret a GitHub issue or feature request.
2. Explore the existing codebase before making changes.
3. Identify the smallest coherent scope of work.
4. Implement the requested change using repository conventions.
5. Add or update tests.
6. Validate the result locally.
7. Prepare output suitable for code review and GitHub Actions auditing.

## Expected Workflow

The default workflow in this repository is:

1. Start from an issue, feature request, or clearly stated acceptance criteria.
2. Inspect the relevant architecture before editing files.
3. Prefer isolated work using `claude --worktree`.
4. Use subagents when they improve clarity or parallelize bounded tasks.
5. Use documentation lookup only when local code is insufficient.
6. Keep changes scoped to the relevant files.
7. Run the relevant tests before finishing.
8. Summarize the changes in PR language.

## Repository Context

This repository contains a full-stack FastAPI template with:

- backend API code
- frontend application code
- authentication and user management
- test suites and developer tooling

The live-session examples are expected to focus primarily on realistic backend tasks such as:

- adding filtering to an endpoint
- adding pagination parameters
- improving request validation
- updating route tests

Typical areas to inspect first:

- `backend/app/api/routes/`
- `backend/app/models.py`
- `backend/app/crud.py`
- `backend/tests/api/routes/`

## Working Rules

When solving issues or feature requests in `full-stack-fastapi-template`, the agent should follow these rules:

1. Do not start editing before identifying the relevant route, model, CRUD, and test files.
2. Prefer extending the existing architecture over inventing new abstractions.
3. Preserve naming, validation, and response patterns already used in the codebase.
4. Avoid unrelated refactors unless the issue explicitly requires them.
5. Keep changes reviewable and limited to the requested scope.
6. If there is uncertainty about framework behavior, use authoritative documentation or mark the uncertainty clearly.
7. If a command, hook, or workflow detail is environment-specific and not confirmed, state that explicitly for the instructor or reviewer.

## Preferred Tools and Features

The agent is expected to use these capabilities when appropriate:

- Claude Code as the main coding assistant
- `claude --worktree` for isolated implementation
- subagents for planner, implementer, tester, or reviewer roles
- GitHub context for issue intake and PR-ready summaries
- Context7 for targeted framework or testing references
- local validation commands such as `pytest`
- GitHub Actions as the audit layer for key workflow steps

## Validation Expectations

Before considering a task complete, the agent should:

1. Run targeted tests for the affected area.
2. Confirm the changed files match the intended scope.
3. Review the diff for unnecessary changes.
4. Produce a concise summary covering:
   - what changed
   - why it changed
   - how it was tested
   - any known uncertainties or follow-ups

## Instructor Notes

If this repository is being used in the workshop session described in the parent `README.md`, the agent behavior should align with that guide.

If any of the following are not known with certainty in the current environment, the agent should state that clearly instead of guessing:

- exact issue URL or issue text
- exact subagent invocation syntax
- exact hook configuration syntax
- exact test command known to pass locally
- exact GitHub Actions workflow used to audit the session
