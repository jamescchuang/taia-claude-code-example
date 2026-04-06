# API Design Rules

Conventions for designing and evolving APIs in this project.

## REST Conventions

- Use nouns for resource paths, not verbs (`/users`, not `/getUsers`)
- Use HTTP methods semantically: GET, POST, PUT, PATCH, DELETE
- Return consistent error shapes: `{ error: { code, message } }`
- Version APIs via URL prefix: `/v1/...`

## Request & Response

- Accept and return JSON by default
- Use camelCase for JSON field names
- Always include a top-level `data` wrapper for successful responses
- Paginated responses include `{ data, pagination: { page, pageSize, total } }`

## Error Codes

- 400 Bad Request — invalid input
- 401 Unauthorized — missing or invalid auth
- 403 Forbidden — authenticated but not allowed
- 404 Not Found — resource does not exist
- 422 Unprocessable Entity — validation failure
- 500 Internal Server Error — unexpected server error

## Backwards Compatibility

- Never remove or rename existing fields — add new ones instead
- Deprecate fields in docs before removing them in a future major version
