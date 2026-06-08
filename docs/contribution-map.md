# Roadmap contribution map

*Non-normative contributor guide. This document turns the roadmap into reviewable contribution shapes. It does not change DACS v0.1 conformance.*

## Use this before opening a PR

DACS separates v0.1 hardening from future standard growth. Most useful community contributions today are either readability improvements, non-normative implementation support, or design issues for future versions.

## Safe editorial/readability PRs

These should preserve all MUST/MUST NOT language, rule IDs, artifact schemas, and conformance semantics.

- Finish readability passes for `spec/DACS-4-SETTLE.md` and `spec/DACS-5-VERIFY.md`.
- Keep DACS-2 §7.9's conformance checklist complete as new rule families are added.
- Split dense normative paragraphs into ordered procedures where the rule text already implies a sequence.
- Improve headings, reader maps, and section-local summaries.
- Fix broken links, stale anchors, typos, and inconsistent terminology.

## Safe non-normative docs

These are good contribution targets because they help implementers without changing conformance.

- Worked examples by stakes: low-value lookup, B2B SaaS, regulated trade.
- Operational builder guidance: finality, float, recovery, key custody, dashboards.
- Artifact/schema index: artifact → section → signature domain → anchor/evidence role.
- Human readability review checklist.
- Spec-reference MCP design docs and read-only tooling proposals.

## Design-issue-first items

Open an issue or discussion before sending a spec PR.

- Fee-split / multi-payee settlement.
- Encrypted-to-parties anchoring for audit/vet records.
- Session-bound settlement evidence for single-chain rails.
- HTLC anti-free-option mechanism.
- Dynamic channel membership.
- Suspicious-pattern flags or minimum-bundle-count reputation advice.
- DACS-X dispute/adjudication semantics beyond the current fixtures.

## Needs reference implementation first

Do not promote these to normative text until a shipped path and reference implementation exist.

- `pay-d402`.
- New payment rails.
- New verification methods.
- New private-channel wire formats.
- New dispute/execution-verification modules.

## Needs substrate primitive or SDK maturity first

These are real roadmap items, but spec changes should follow substrate capability maturity.

- Liquidity Tank Phase 2–4 expansion.
- CCI-keyed L2PS membership and transcript export.
- DAHR validator-body-signed mode.
- Native multi-party Storage Program signature helper.

## Do not PR directly without steward direction

- New conformance obligations for v0.1.
- Artifact schema changes that existing implementations must accept/reject differently.
- New closed-registry entries.
- Normative governance changes.
- Anything that changes settlement, reputation, or privacy semantics.

## What a high-signal PR includes

- Exact files and sections touched.
- Statement that the PR is normative or non-normative.
- If editorial: statement that no rule IDs, schemas, or MUST/MUST NOT obligations changed.
- Test plan with the local validators from `README.md`.
- For roadmap items: link to the relevant `ROADMAP.md` row.
