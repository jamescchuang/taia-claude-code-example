# Security Review Checklist

## Injection

- [ ] SQL injection: are all queries parameterized or using an ORM?
- [ ] Command injection: is user input ever passed to shell commands?
- [ ] XSS: is user-supplied content properly escaped before rendering?
- [ ] Template injection: are templates rendered with user-controlled data?

## Authentication & Authorization

- [ ] Are all endpoints protected by authentication where required?
- [ ] Is authorization checked at the resource level (not just route level)?
- [ ] Are JWTs validated (signature, expiry, audience)?
- [ ] Are session tokens rotated after privilege changes?

## Sensitive Data

- [ ] Are secrets read from environment variables, not hardcoded?
- [ ] Is PII logged or exposed in error messages?
- [ ] Are passwords hashed with a strong algorithm (bcrypt, argon2)?
- [ ] Is sensitive data encrypted at rest and in transit?

## Input Validation

- [ ] Is all external input validated and sanitized?
- [ ] Are file uploads restricted by type and size?
- [ ] Are URL redirects validated against an allowlist?

## Dependencies

- [ ] Do new dependencies have known CVEs?
- [ ] Are dependency versions pinned?

## Error Handling

- [ ] Do error responses avoid leaking stack traces or internal details?
- [ ] Are all exceptions caught and handled gracefully?
