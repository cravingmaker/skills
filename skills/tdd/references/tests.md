# Good and bad tests

Read this when writing or changing a test. Adapted from Matt Pocock's tdd/tests.md, Superpowers' writing-good-tests.md and pstack's test-behavior principle.

## Contents

- [Good tests](#good-tests)
- [Bad tests](#bad-tests)
- [The contract decides](#the-contract-decides)
- [Gate before the test body](#gate-before-the-test-body)
- [Mutation check](#mutation-check)
- [Warning signs](#warning-signs)

## Good tests

**Integration-style**: test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses the public interface only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

Prefer table-driven tests with literal expected values when one behavior has several input cases.

## Bad tests

**Implementation-detail tests**: coupled to internal structure.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on internal call counts or order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of the interface

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: the expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

**Behavior, not text.** Asserting that a script, config or document contains an exact line proves only that the source is the source. Run a script against controlled inputs and assert its outputs, side effects or exit codes.

**Your code, not the framework.** Test the contract your code makes at its seams (the route you register, the query you emit, the payload you produce), not the framework's own mechanics. Constructors, getters, constants and plain forwarding earn tests only when they validate, normalize, default, derive, enforce or cause side effects.

## The contract decides

The contract decides what is behavior, not the shape of the assertion.

- When "an empty cart never charges" is the promise, asserting the payment client got no call is behavior. Pair it with a case where the charge happens, so the test shows it can see a call.
- The payload a mocked external service receives is behavior, because that service observes it. A call to an internal helper is implementation.
- An empty list is the exact answer when no record matches, and a hollow check when the test only needs some result.
- An exact error message pins wording no caller reads; the error type callers branch on is the contract.
- A test can pin an invariant instead of a call, such as a key that must exist in two tables or a compile-time type check.

## Gate before the test body

```
Name the production change that would make this test fail.
  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior that depends on them
Confirm the expected value is derived without the code under test.
  If it reuses the code's logic or helpers → replace it with a literal or hand-checked fixture
```

## Mutation check

Before finishing, mentally mutate the production code; at least one test should fail for each realistic mutation:

- Wrong constant or argument
- Wrong branch handler
- Missing state change or side effect
- Empty or default return
- Missing validation for zero, empty, nil, unauthorized or malformed input

A mutation nothing catches marks the behavior as unprotected, or the test as tautological.

## Warning signs

- Setup and assertion share the same object, guaranteeing equality
- The test can fail only through a crash or a missing selector
- The test fails on every intentional change and never on accidental breakage
- Expected values are hidden behind loops, builders or helpers
- The test exists for coverage and checks no outcome
- Mock setup is more than half the test, or you can't explain why the mock is needed
