# Z: CI/CD Pipeline

## GitHub Actions Workflows

### Build & Test (every push)
```
trigger: push to any branch (except main docs changes)
  ├── lint (golangci-lint/eslint/pylint)
  ├── unit tests (go test / jest / pytest)
  ├── build (Docker image)
  ├── security scan (trivy + snyk)
  └── upload artifact (Docker image to registry)
```

### CI (pull request)
```
trigger: PR opened / updated
  ├── build & test (same as above)
  ├── integration tests (docker-compose + test DB)
  └── deploy preview env (PR-specific, auto-destroy on merge)
```

### CD (deploy)
```
trigger: push to main / tag v*
  ├── build & test
  ├── semantic-release (auto-changelog + version bump)
  ├── deploy staging (helm upgrade —install)
  ├── smoke tests (see smoke-test-checklist.md)
  ├── approval gate (manual for prod, auto for staging)
  ├── deploy production (canary 10% → 50% → 100%)
  ├── smoke tests (production)
  └── notify Slack (#deployments channel)
```

## Artifact Management
- Docker images: `registry.example.com/<service>:<git-sha>` (immutable)
- Helm charts: `oci://registry.example.com/charts/<service>`
- npm/pip packages: private registry (GitHub Packages / Artifactory)
- Retention: keep last 100 builds, all tagged releases

## Deployment Environments
| Environment | Purpose | Auto-deploy | Approval |
|------------|---------|-------------|----------|
| Preview    | Per-PR testing | Yes | None |
| Staging    | Pre-prod validation | On main merge | None |
| Production | Live | On tag/release | Manual gate |

## Approval Gates
- **Staging smoke tests** must pass before prod approval prompt
- **Prod approval**: requires @oncall-eng + @em from affected service
- **Emergency bypass**: S0/S1 hotfix (see hotfix-procedure.md)
