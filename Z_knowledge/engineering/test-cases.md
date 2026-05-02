# Z: Test Case Writing Guide

## Format (BDD-style)
```
Feature: User login
  Scenario: Successful login with valid credentials
    Given a registered user with email "test@example.com"
    When they submit login with correct password
    Then they receive a 200 response with a JWT token
```

## Coverage Targets
- Unit: ≥85% line coverage, ≥90% branch coverage on core logic
- Integration: all public API endpoints (200 + 4xx + 5xx)
- E2E: critical user journeys (login, purchase, search, signup)
- No coverage targets for UI boilerplate or generated code

## Boundary Analysis
- Test at boundaries: 0, 1, max-1, max, max+1 for numeric inputs
- Empty strings, nulls, very long strings (>10K chars)
- Date ranges: past, present, future, leap year, timezone edges

## Equivalence Partitioning
- Divide input domain into valid/invalid partitions
- One test per partition is sufficient
- Example: age (0-17 invalid, 18-120 valid, >120 invalid)

## Test Data Management
- Use factories (FactoryBoy) rather than hardcoded fixtures
- Clean up test data after each run (transaction rollback)
- Never share mutable test data between tests
- Seed data for integration tests: minimal, versioned

## Naming Conventions
- `test_{function_name}__{scenario}__{expected_result}`
- Example: `test_create_order__with_expired_card__returns_402`
- Negative tests prefixed: `test_{fn}__fails_when_{condition}`
