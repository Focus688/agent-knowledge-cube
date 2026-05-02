# Z: Security Guidelines

## Input Validation
- Validate all input at API boundary (type, range, length, format)
- Whitelist > blacklist — allow known-good patterns only
- Sanitize file uploads: limit size, check MIME, scan for malware
- Use structured parsers (no eval, no shell interpolation)

## Authentication & Authorization
- OAuth 2.0 / OIDC for external auth; JWT for service-to-service
- Short-lived tokens (15min access, 7d refresh with rotation)
- RBAC: least privilege per service account and user role
- API keys scoped to specific actions; rotate on leak

## Data Encryption
- TLS 1.3 for all in-transit traffic (no HTTP internally either)
- AES-256 for data at rest; envelope encryption with KMS
- Encrypt PII fields at application level (column-level)
- Hash passwords with bcrypt/argon2 (not MD5/SHA)

## Dependency Security
- Automated scanning: Dependabot + Snyk on every PR
- Pin all dependencies (no floating versions)
- Weekly CVE audit; critical CVEs patched within 24h
- SBOM generation for each release

## Secrets Management
- Use Vault / AWS Secrets Manager / K8s External Secrets
- Never commit secrets to git — detect with pre-commit hooks
- Rotate secrets on incident; audit access logs

## OWASP Top 10 Awareness
- Track: A01 (Broken Access), A03 (Injection), A07 (Auth Failures)
- Regular pentests; SAST/DAST in CI pipeline
