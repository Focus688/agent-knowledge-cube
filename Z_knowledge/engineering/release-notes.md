# Z: Release Notes Process

## Version Numbering
- **SemVer**: `MAJOR.MINOR.PATCH` (e.g., 2.4.1)
  - MAJOR: breaking API changes
  - MINOR: new features, backwards-compatible
  - PATCH: bug fixes, security patches
- Pre-release suffix: `-alpha.1`, `-beta.2`, `-rc.3`
- Build metadata: `+build.20260415`

## Changelog Format (Keep a Changelog)
```markdown
# Changelog
## [2.4.1] - 2026-04-15
### Added
- New endpoint: GET /api/v2/users/:id/profile
### Changed
- Pagination limit increased from 50 to 100
### Fixed
- Fixed race condition in order cancellation (#892)
### Security
- Upgraded jwt library to v5.2.0 (CVE-2026-1234)
### Deprecated
- POST /api/v1/orders (use /api/v2/orders instead)
```

## Breaking Changes
- Listed at the top of release notes with migration instructions
- Include removal date + affected consumers
- Example: "API v1 will be removed on 2026-07-01. Migrate to API v2."

## Migration Guides
- One guide per breaking change
- Before/after code snippets
- Tooling: provide codemods or migration scripts when possible

## Deprecation Notices
- Add `Deprecated` header or warning response header
- Sunset header: `Sunset: Sat, 01 Jul 2026 00:00:00 GMT`
- Log deprecation warnings to monitoring (track usage)
