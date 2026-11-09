# When to mock

Read this when adding a mock, fake or test helper. Adapted from Matt Pocock's tdd/mocking.md and Superpowers' writing-good-tests.md.

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes; prefer a test database)
- Time and randomness
- File system (sometimes)

Don't mock:

- Your own classes or modules
- Internal collaborators
- Anything you control

## Mock at the right level

Learn every side effect of the real method before replacing it. Mock the slow or external operation and keep real what the test depends on. When unsure, run the test against the real implementation first and observe what actually needs to happen.

```typescript
// BAD: the mock swallows the config write that duplicate detection reads
vi.mock("ToolCatalog", () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined),
}));

// GOOD: mock only the slow server startup; the config write stays real
vi.mock("MCPServerManager");
```

- **The mock earns no assertions.** An assertion on the mock itself passes when the mock is present and says nothing about the code. Assert the real behavior, or unmock it.
- **Make doubles specific.** When arguments, call counts or ordering are part of the contract with the external system, assert them. Give each branch (success, error, malformed) its own fixture, so the wrong branch cannot satisfy the expectation.
- **Mirror real data completely.** A mock response carries the full documented structure, not just the fields this test reads; partial mocks pass while integration breaks.
- **Production classes carry production methods only.** Cleanup that only tests need lives in test utilities.
- **Prefer real components over complex mocks.** When mock setup outgrows the test logic, switch to an integration test with real components.

## Designing for mockability

At system boundaries, design interfaces that are easy to mock.

**1. Use dependency injection.** Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers.** Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means each mock returns one specific shape, test setup has no conditional logic, it is easy to see which endpoints a test exercises, and each endpoint keeps its own types.
