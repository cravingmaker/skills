# Service boundaries

Read this when independent deployment or isolation is the disputed benefit.

Compare the current service, a focused modular repair, and an extraction only when each is viable. An extraction needs a measurable reason: independent scaling, deployment cadence, failure isolation, security isolation, or team ownership. Count compatibility, observability, on-call, provisioning, partial failure, and migration costs in the comparison.

Trace a representative operation through both proposed boundaries. Check whether they require shared writes, lockstep releases, synchronous call chains, or coordinated rollback. Those dependencies limit the independence being claimed. One owning writer and a stable contract can be useful inside a single deployment; network calls alone do not create autonomy.

Before recommending a split, demonstrate deployment and recovery readiness and name the data authority during coexistence. Keep rollback or forward repair and the removal condition for temporary adapters explicit.

Methods are paraphrased from Fowler's [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html), [Microservice Premium](https://martinfowler.com/bliki/MicroservicePremium.html), and [Microservice Prerequisites](https://martinfowler.com/bliki/MicroservicePrerequisites.html).
