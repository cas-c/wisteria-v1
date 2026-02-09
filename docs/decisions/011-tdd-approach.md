# ADR-011: Test-Driven Development for Future Phases

**Status:** Accepted

**Context:** Phase 2 was built code-first: implement features, then write tests at the end. This worked but had drawbacks:

1. Tests were written to match existing behavior, not to define expected behavior. They caught bugs *after* the fact rather than preventing them.
2. Some edge cases (duplicate slugs, buying unavailable products) were discovered during testing and required going back to fix the implementation.
3. Without tests as a safety net during development, refactoring was riskier.

Going forward, we want a more disciplined approach as the codebase grows.

**Decision:** Adopt TDD (Red-Green-Refactor) for backend services and API routes starting in Phase 3.

**How it works:**

1. **Red:** Write a failing test that describes the desired behavior.
2. **Green:** Write the minimum code to make the test pass.
3. **Refactor:** Clean up the implementation while tests stay green.

**Where TDD applies:**
- Backend service functions (business logic) — always TDD.
- API route behavior (status codes, response shapes, auth) — always TDD.
- Database models — no TDD needed. Models are declarative; test them through service tests.
- Frontend components — component tests and integration tests are written alongside or after. TDD is awkward for visual UI work; use Playwright for end-to-end flows.

**Where TDD does NOT apply:**
- One-off scripts (seed, migrations).
- Configuration files.
- Styling and layout (test visually, not with assertions).

**Practical workflow for a new backend feature:**
```
1. Write the Pydantic schema (request/response shapes)
2. Write test cases for the service function (they fail — function doesn't exist)
3. Implement the service function until tests pass
4. Write test cases for the route (they fail — route doesn't exist)
5. Implement the route, wire up the service
6. Refactor if needed, re-run tests
```

**Reasoning:**
- Forces thinking about edge cases and error conditions upfront.
- Tests serve as living documentation of expected behavior.
- Refactoring is safer — you know immediately if you broke something.
- Matches how senior engineers are expected to work in production codebases.

**Trade-off:** Slower initial velocity — you write tests before you have working code, which feels backwards at first. But it pays back quickly: fewer bugs, less back-and-forth, and more confidence when changing code.

**What we're NOT doing:**
- 100% coverage targets. Coverage is a lagging indicator, not a goal. Test behavior, not lines.
- Testing implementation details. Tests should assert *what* happens, not *how*. If we refactor internals, tests shouldn't break.
- Mocking everything. We use real database calls in tests (against `wisteria_test`). Mocks hide real bugs.
