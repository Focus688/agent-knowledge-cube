# Z: Technical Feasibility Assessment

## Template Structure

### 1. Problem Statement
- What are we trying to build? (1-2 sentences)
- Which user problem does this solve?
- Links to product requirement doc, design spec, or ticket

### 2. Effort Estimation
- **Engineering effort**: person-weeks (frontend/backend/infra)
- **Complexity**: Low / Medium / High / Unknown
  - Low: well-known pattern, existing libraries
  - Medium: needs some research, moderate integration
  - High: novel approach, heavy R&D needed
  - Unknown: major unknowns that need spike/prototype

### 3. Dependency Analysis
| Dependency | Status | Risk |
|-----------|--------|------|
| Internal service X API | Available | Low |
| External vendor Y | Contract pending | High |
| Database migration | Needs review | Medium |

### 4. Risk Assessment
- **Technical risk**: unfamiliar stack, performance constraints, scale unknown
- **Schedule risk**: dependencies on external teams, regulatory approvals
- **Security risk**: data handling, compliance (SOC2/GDPR/HIPAA)
- **Mitigation**: spike to reduce unknowns, parallel workstreams

### 5. Alternative Approaches
- **Approach A** (recommended): full build — best long-term, more upfront effort
- **Approach B**: use existing vendor — faster but higher cost/vendor lock-in
- **Approach C**: incremental build — MVP in 2 weeks, iterate from there
- Trade-off summary: cost vs. speed vs. quality vs. maintainability

### 6. Go/No-Go Recommendation
- Clear recommendation with rationale
- Blockers highlighted (red flags that must be addressed first)
