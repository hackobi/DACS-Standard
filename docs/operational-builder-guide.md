# Operational builder guide

*Non-normative. This guide helps operators prepare a DACS implementation for production. It complements the [builders guide](./builders-guide.md) by focusing on operational, capital, and settlement-finality questions that the v0.1 specification deliberately leaves to implementers.*

## 1. Scope and assumptions

Before implementing, write down the local operating profile:

- Which DACS stages your system produces, consumes, or both.
- Which substrate satisfies SR-1 through SR-5 for each listing class.
- Which rails and recipes are enabled, disabled, or operator-gated.
- Which local policies are stricter than DACS conformance.
- Which evidence you will retain outside anchored artifacts for incident response.

Keep this profile separate from normative conformance. A local policy may reject a session that DACS would allow; it should not claim the protocol itself requires that rejection.

## 2. Capital and float planning

Settlement failures often come from ordinary operations, not protocol ambiguity. Plan capital by rail.

For each rail, track:

- asset and chain/network;
- expected session volume;
- confirmation/finality time;
- refund or recovery window;
- gas, relay, bridge, facilitator, and treasury fees;
- worst-case concurrent exposure;
- who funds each cost: buyer, seller, orchestrator, or platform.

Recommended operator practice:

- Keep reserved float for pending sessions separate from treasury balances.
- Preflight spendable balance before advertising or accepting a rail.
- Maintain a per-rail minimum-reserve threshold.
- Alert before threshold breach, not after a session has committed.
- Include retries and stuck transactions in exposure modelling.

## 3. Undercapitalised mid-session behavior

Undercapitalisation is an operational failure that should be surfaced early and classified consistently.

Recommended flow:

1. Run balance and allowance preflight before selecting a rail.
2. If the selected rail cannot be funded before commitment, fail fast before external effects.
3. If undercapitalisation appears after commitment, preserve the phase result and classify through the relevant phase `errorClass`.
4. Do not fabricate successful SettlementEvidence to hide operator shortfall.
5. Preserve enough local diagnostic evidence to explain whether the fault was local policy, counterparty action, substrate failure, or rail unavailability.

The spec defines evidence and error classes; the operator defines treasury and retry policy.

## 4. Settlement finality integration

Do not mark `ok: true` until the rail-specific finality condition is satisfied.

For each rail, document:

- confirmation threshold;
- reorg depth considered safe;
- timeout before retry or pause;
- recovery window;
- explorer or provider APIs used for monitoring;
- whether finality is probabilistic, economic, or protocol-final.

Dashboard signals should distinguish:

- pending broadcast;
- included but below threshold;
- final;
- reorged;
- expired/refundable;
- recovery-pending;
- terminal failure.

Plan for the roadmap candidate `SettlementFinality` field without depending on it in v0.1.

## 5. Chain reorganizations and recovery windows

Operators should treat chain reorgs and bridge/tank recovery windows as first-class incidents.

Recommended runbook:

1. Freeze local progression for the affected session.
2. Re-check the rail's authoritative source.
3. If evidence was not yet anchored, wait for the replacement/finality state before anchoring.
4. If evidence was anchored and later contradicted by a reorg, open an amendment or implementation report as appropriate; do not silently rewrite history.
5. Record incident timing, chain references, and operator decision points.

For cross-chain rails, separate "value moved" from "evidence anchored." SR-2 availability problems after value movement should follow the DACS-5 pause/resume semantics rather than being treated as ordinary counterparty failure.

## 6. Key custody and HSM practice

Inventory keys by artifact and authority:

- listing signing keys;
- identity-bundle presentation keys;
- session/channel keys;
- agreement signing keys;
- settlement evidence signer keys;
- rating signer keys;
- bundle closeout keys;
- recipe/rail steward keys if applicable;
- treasury and payment keys.

Recommended controls:

- Use HSM or remote-signer controls for treasury, steward, and production operator keys.
- Keep domain-separated signing payload logs so signature bugs are diagnosable.
- Rotate session keys without changing primary-claim reputation keying.
- Separate hot operational keys from registry/steward keys.
- Require human approval for steward-key use while PA-2 single-signer governance remains in force.

## 7. Observability and incident response

Monitor at least:

- anchored write failures;
- verifier timeouts and warning rates;
- recipe/rail availability changes;
- payment rail preflight failures;
- finality delays;
- cross-chain asymmetric states;
- abort rates by counterparty and listing;
- bundle production failures;
- signature-verification failures.

Alerts should include the DACS phase, `jobId`, party primary claim where safe to show, rail or recipe ID, error class, and latest tx/evidence reference.

## 8. Error-class playbooks

Use local runbooks that mirror DACS error classes:

- **transient:** retry within budget; do not mutate committed artifacts until retry outcome is known.
- **permanent:** stop retrying; produce failure evidence where the phase requires it.
- **counterparty:** preserve the evidence needed for reputation derivation and possible dispute review.
- **substrate:** pause when the spec permits pause/resume; avoid misclassifying substrate outage as counterparty fault.
- **settlement-atomicity:** escalate immediately; identify which external leg moved and which did not.

## 9. Local fixtures and release gates

Before release:

- Run the local validators listed in `README.md`.
- Maintain fixtures for happy path, failed Vet, failed payment, aborted session, and cross-chain recovery/asymmetry where supported.
- Test that dashboards link back to anchored artifacts and external tx references.
- Record implementation deviations as local policy notes, not spec assumptions.
- Open implementation reports when production behavior reveals ambiguity in the standard.
