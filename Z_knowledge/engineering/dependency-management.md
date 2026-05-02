# Z: Dependency Management

## Version Pinning Policy
- **No floating versions**: pin exact versions in `package.json` (npm), `go.sum` (Go), `requirements.txt` (Python)
- **Lockfiles**: commit `package-lock.json`, `go.sum`, `poetry.lock`, `Gemfile.lock` to git
- **Exceptions**: internal libraries use `>=1.2.3 <2.0.0` range with lockfile
- **Auto-updates**: Dependabot/Auto-merge for patch versions only (after CI passes)

## Security Scanning
### Dependabot (GitHub native)
- Scans every PR for vulnerable dependencies
- Auto-opens PRs for non-breaking security updates
- Weekly digest of all dependency updates
- Alerts: Dashboard + email + Slack webhook

### Snyk (deep scanning)
- Monitors for license compliance (GPL/AGPL flagged)
- Container image scanning (trivy in CI as well)
- IaC scanning (Terraform/K8s manifests for misconfigs)
- Policy: block PRs with High/Critical severity vulnerabilities

## Update Cadence
| Type | Cadence | Review Required |
|------|---------|----------------|
| Security patches | Within 24h of CVE disclosure | Expedited review |
| Patch updates | Weekly (automated PRs) | Auto-merge if tests pass |
| Minor updates | Monthly | Human review |
| Major updates | Quarterly (with migration plan) | Architecture review |
| Internal libs | On-demand, per feature need | Standard PR review |

## Deprecation Handling
- **Deprecated deps**: audit quarterly for unmaintained libraries
- **Replacement criteria**: active maintenance (commits in last 6mo), community size, security track record
- **Migration process**:
  1. File issue: `deprecate: replace <lib> with <replacement>`
  2. Implement replacement behind feature flag
  3. Verify in staging for 1 week
  4. Remove old dependency + feature flag

## SBOM (Software Bill of Materials)
- Generate SPDX or CycloneDX SBOM with every release (via CI)
- Store SBOM alongside Docker image in registry
- Required for SOC 2 / FedRAMP compliance
- Tool: `syft` (generation) + `grype` (vulnerability scanning)
