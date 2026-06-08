# Human readability review checklist

*Non-normative. Use this checklist when reviewing the spec-compression / readability work. The target reader is technically astute and comfortable with specifications; the goal is clarity, not beginner training.*

## First principle

Preserve normative meaning. A readability PR should make the existing rule easier to understand without changing what an implementation MUST accept, reject, sign, anchor, or derive.

## Section-level checks

- Does the section state the purpose before edge cases?
- Is the main procedure in ordered steps when order matters?
- Are rule families grouped so each rule ID is easy to cite?
- Are long paragraphs split without changing conditions or precedence?
- Are examples explicitly marked non-normative?
- Is every cross-reference useful and resolvable?
- Can a reviewer tell which role is responsible: party, orchestrator, verifier, steward, consumer, or implementer?

## Normative-preservation checks

- No MUST / MUST NOT / SHOULD / MAY obligation was added, removed, or weakened accidentally.
- No closed-registry entry was added or renamed.
- No artifact schema field changed meaning.
- No signature domain separator changed.
- No anchoring address pattern changed.
- No conformance rule ID was dropped from summaries or indexes.
- No roadmap candidate is phrased as shipped v0.1 behavior.

## Table checks

Tables are useful but dangerous. They can create contradictions by adding derived columns not present in the prose.

Before adding or editing a table:

- Verify each row against the original normative prose.
- Avoid derived summaries that hide precedence rules.
- Keep edge-case notes in the prose when a compact table would over-simplify them.
- If the table is informative, label it as such.
- If the table is normative, say exactly which rule it enumerates.

## Examples and diagrams

- Use examples to show shape, not to define new behavior.
- Include enough artifact names that readers can map the example back to the spec.
- Avoid invented fields unless clearly labelled pseudocode.
- If an example conflicts with the normative section, fix the example.

## Reviewer feedback format

High-signal feedback names:

1. File and section.
2. The confusing passage.
3. The alternative reading a competent implementer might take.
4. Suggested wording or structural change.
5. Whether the issue is editorial, conformance-affecting, or a roadmap/design item.

## Final pre-merge checklist

- Run `python3 scripts/validate-docs.py`.
- Run `python3 scripts/validate_rule_ids.py` if labelled rules or indexes changed.
- Run the full local validation command set from `README.md` before merging broad readability work.
- In the PR body, explicitly state whether the change is normative or non-normative.
