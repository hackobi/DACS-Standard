# DACS spec-reference MCP design

*Non-normative design note. This proposes a read-only MCP server for navigating the DACS specification. It does not define conformance behavior.*

## Goal

Expose the DACS spec as a version-stamped reference service for agents, editors, and implementation tools. The server answers questions like "where is HTLC-7 defined?" or "what signature domain applies to AttestationBundle?" without inventing rules or mutating repository state.

## Non-goals

- No conformance decisions beyond returning existing spec text and vector metadata.
- No writing to the repository.
- No automatic PR generation.
- No registry-steward authority.
- No hidden interpretation layer; every response cites source file and section.

## Data sources

- `spec/CORE.md`
- `spec/DACS-1-IDENTIFY.md`
- `spec/DACS-2-VET.md`
- `spec/DACS-3-NEGOTIATE.md`
- `spec/DACS-4-SETTLE.md`
- `spec/DACS-5-VERIFY.md`
- `spec/PROFILE.md`
- `docs/rule-id-index.md`
- `docs/artifact-index.md`
- `conformance/vectors/`
- `CHANGELOG.md`
- `ROADMAP.md`

## Version stamping

Every response should include:

- profile: `DACS v0.1`
- source commit SHA when available
- source file path
- section heading or anchor
- whether the source is normative or non-normative

## Proposed tools

### `lookup_rule`

Input: rule ID or rule family, e.g. `HTLC-7`, `SIG-1`, `RAV-R4`.

Output:

- defining section
- exact excerpt
- linked conformance-plan row if present
- vector paths if present

### `lookup_artifact`

Input: artifact/type name, e.g. `AgreementDocument`, `SettlementEvidence`, `AttestationBundle`.

Output:

- defining module and section
- signature domain separator if applicable
- anchor/evidence role
- related conformance hooks
- example vector path if present

### `resolve_section`

Input: section reference, e.g. `§9.5.4`.

Output:

- file path
- heading
- excerpt or whole section depending on size

### `search_spec`

Input: query string.

Output:

- ranked snippets from normative spec files first
- non-normative docs second
- source labels for each result

### `list_registry_entries`

Input: registry name: `identity-schemes`, `verification-methods`, `recipes`, `rails`, `negotiation-patterns`, `delivery-phases`.

Output:

- entries as currently documented
- source table location
- note when entries are closed v0.1 scope

### `list_vectors`

Input: optional rule ID, artifact, or vector category.

Output:

- vector file path
- expected result
- linked rule refs

## Safety and correctness rules

- Prefer quoting the spec over paraphrase.
- Mark non-normative material explicitly.
- If two sources conflict, report the conflict and cite both; do not choose silently.
- Do not infer conformance from roadmap candidates.
- Do not treat examples as normative.

## Implementation outline

1. Parse Markdown headings and anchors from `spec/` and selected `docs/` files.
2. Build indexes for section refs, labelled rules, artifact names, domain separators, and vector `ruleRefs`.
3. Serve read-only MCP tools backed by those indexes.
4. Add a repository validator that fails if the generated MCP index cannot resolve a rule or section already referenced by `docs/rule-id-index.md` or `docs/artifact-index.md`.
5. Keep generated indexes deterministic so CI can compare committed output.

## Open questions before implementation

- Should excerpts preserve line numbers, anchors, or both?
- Should the server include roadmap rows by default, or require an explicit `includeRoadmap` flag?
- Should rule-family lookup return every member rule or only the defining section?
- Should vectors be treated as canonical only under `conformance/vectors/`, excluding `conformance/fixtures/` by default?
